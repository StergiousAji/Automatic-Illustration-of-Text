from PIL import Image
from transformers import CLIPTokenizerFast, CLIPProcessor, CLIPModel, AutoTokenizer
from multilingual_clip import pt_multilingual_clip
from tqdm.auto import tqdm
import numpy as np
import os
import torch

class CLIP:
    # Load pre-trained multi-lingual CLIP model on instantiation
    def __init__(self, image_paths, image_vectors_path,  folder='.', multilingual=False, model_id="openai/clip-vit-base-patch32", multilingual_model_id="M-CLIP/XLM-Roberta-Large-Vit-B-32"):
        self.device = "cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu")
        
        self.model_id = model_id
        self.multilingual = multilingual
        self.multilingual_model_id = multilingual_model_id

        if multilingual:
            self.model = pt_multilingual_clip.MultilingualCLIP.from_pretrained(multilingual_model_id)
            self.tokeniser = AutoTokenizer.from_pretrained(multilingual_model_id)
        else:
            self.model = CLIPModel.from_pretrained(self.model_id).to(self.device)
            self.tokeniser = CLIPTokenizerFast.from_pretrained(self.model_id)
        
        self.processor = None

        self.image_folder = folder
        self.image_paths = np.array(image_paths)
        self.load_image_vectors(image_vectors_path)
    
    def process_images(self, image_vectors_path, batch_size=16):
        self.processor = CLIPProcessor.from_pretrained(self.model_id)

        self.image_vectors = None
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

                self.image_vectors = np.concatenate((self.image_vectors, batch_embeddings)) if self.image_vectors is not None else batch_embeddings
            except Exception as ex:
                print(f"\u001b[31m{type(ex).__name__}: {ex.args}\u001b[0m")

        if self.image_vectors is not None:
            print(self.image_vectors.shape)
            self.image_vectors = normalise(self.image_vectors)

            np.save(image_vectors_path, self.image_vectors)

    def query_prompt(self, prompt, top=10):
        text_embeddings = None

        if not self.multilingual:
            inputs = self.tokeniser(prompt, return_tensors="pt").to(self.device)
            text_embeddings = self.model.get_text_features(**inputs).cpu().detach().numpy()
        else:
            text_embeddings = self.model.forward(prompt, self.tokeniser).cpu().detach().numpy()

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


# Walk through given directory structure to index each image. 
# Assumes ImageNet train directory structure, can be set to False.
def index_image_paths(folder, imagenet=True):
    try:
        image_paths = []

        if imagenet:
            for synset in os.listdir(folder):
                subfolder = os.path.join(folder, synset)
                if os.path.isdir(subfolder):
                    for image_name in os.listdir(subfolder):
                        image_paths.append(os.path.join(synset, image_name))
        else:
            return os.listdir(folder)
    except Exception as ex:
        print(f"\u001b[31m{type(ex).__name__}: {ex.args}\u001b[0m")

    return image_paths


def get_images_batch(folder, image_paths, start, end):
    return [Image.open(os.path.join(folder, path)) for path in image_paths[start:end]]

def close_batch(batch):
    for image in batch:
        image.close()

def normalise(matrix):
    return matrix / np.linalg.norm(matrix, axis=0)