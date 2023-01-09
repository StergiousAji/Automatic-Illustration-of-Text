from PIL import Image
from transformers import CLIPTokenizerFast, CLIPProcessor, CLIPModel
from tqdm.auto import tqdm
import numpy as np
import os
import pickle
import torch

from datasets import load_dataset

class CLIP:
    # Load pre-trained CLIP on instantiation.
    def __init__(self, image_paths, folder=None, model_id="openai/clip-vit-base-patch32"):
        self.device = "cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu")
        
        self.model_id = model_id
        self.tokeniser = CLIPTokenizerFast.from_pretrained(model_id)
        self.processor = None
        self.model = CLIPModel.from_pretrained(model_id).to(self.device)

        self.image_folder = folder
        self.image_paths = np.array(image_paths)
        self.image_vectors = None
    
    def process_images(self, image_vectors_path, batch_size=16):
        self.processor = CLIPProcessor.from_pretrained(self.model_id)
        img_vectors = None
        for i in tqdm(range(0, len(self.image_paths), batch_size)):
            try:
                images_batch = get_images_batch(self.image_folder, self.image_paths, i, i+batch_size)

                batch = self.processor(
                    text=None,
                    images=images_batch,
                    return_tensors="pt",
                    padding=True
                )["pixel_values"].to(self.device)

                close_batch(images_batch)

                batch_embeddings = self.model.get_image_features(pixel_values=batch).squeeze(0)
                batch_embeddings = batch_embeddings.cpu().detach().numpy()

                img_vectors = np.concatenate((img_vectors, batch_embeddings)) if img_vectors is not None else batch_embeddings
            except Exception as ex:
                print(f"\u001b[31m{type(ex).__name__}: {ex.args}\u001b[0m")

        if img_vectors is not None:
            print(img_vectors.shape)
            img_vectors = normalise(img_vectors)

            self.image_vectors = img_vectors
            np.save(image_vectors_path, img_vectors)

    def query_prompt(self, prompt, top=10):
        inputs = self.tokeniser(prompt, return_tensors="pt").to(self.device)
        text_embeddings = self.model.get_text_features(**inputs).cpu().detach().numpy()

        # Compute cosine similarity scores between prompt text and images
        scores = np.dot(text_embeddings, self.image_vectors.T)

        most_similar = np.argsort(-scores[0])[:top].tolist()
        for i in most_similar:
            print(f"\n{self.image_paths[i]} ({i}): {scores[0][i]}")
        
        return most_similar
    
    def load_image_vectors(self, image_vectors_path, exclude=[]):
        if not os.path.exists(image_vectors_path):
            print("Processing images...")
            self.process_images(image_vectors_path)
        else:
            self.image_vectors = np.load(image_vectors_path)

# Walk through imagenet directory structure to index each image.
def index_image_paths(folder):
    image_paths = []
    for synset in os.listdir(folder):
        subfolder = os.path.join(folder, synset)
        if os.path.isdir(subfolder):
            for image_name in os.listdir(subfolder):
                image_paths.append(os.path.join(synset, image_name))

    return image_paths


def get_images_batch(folder, image_paths, start, end):
    return [Image.open(os.path.join(folder, path)) for path in image_paths[start:end]]

def close_batch(batch):
    for image in batch:
        image.close()

def normalise(matrix):
    return matrix / np.linalg.norm(matrix, axis=0)