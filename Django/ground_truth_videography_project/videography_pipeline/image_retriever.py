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
    def __init__(self, folder, model_id="openai/clip-vit-base-patch32"):
        self.device = "cuda" if torch.cuda.is_available() else ("mps" if torch.backends.mps.is_available() else "cpu")

        self.tokeniser = CLIPTokenizerFast.from_pretrained(model_id)
        self.processor = CLIPProcessor.from_pretrained(model_id)
        self.model = CLIPModel.from_pretrained(model_id).to(self.device)

        self.image_paths = get_image_paths(folder, True)
    
    def process_images(self, batch_size=16):
        img_vectors = np.array([])
        for i in tqdm(range(0, len(self.image_paths), batch_size)):
            try:
                images_batch = get_images_batch(self.image_paths, i, i+batch_size)

                batch = self.processor(
                    text=None,
                    images=images_batch,
                    return_tensors="pt",
                    padding=True
                )["pixel_values"].to(self.device)

                close_batch(images_batch)

                batch_embeddings = self.model.get_image_features(pixel_values=batch).squeeze(0)
                batch_embeddings = batch_embeddings.cpu().detach().numpy()

                img_vectors = np.concatenate((img_vectors, batch_embeddings))

                # if img_vectors is None:
                #     img_vectors = batch_embeddings
                # else:
                #     img_vectors = np.concatenate((img_vectors, batch_embeddings))
            except Exception as ex:
                print(ex)

        print(img_vectors.shape)

        return normalise(img_vectors)

    def query_prompt(self, prompt, img_vectors, top=10):
        inputs = self.tokeniser(prompt, return_tensors="pt")
        text_embeddings = self.model.get_text_features(**inputs).cpu().detach().numpy()

        # Compute cosine similarity scores between prompt text and images
        scores = np.dot(text_embeddings, img_vectors.T)

        most_similar = np.argsort(-scores[0])[:top].tolist()
        for i in most_similar:
            print(f"\n{self.image_paths[i]} ({i}): {scores[0][i]}")
        
        return most_similar

# Walk through imagenet directory structure to index each image.
# TODO: DELETE TEST FLAG WHEN REAL IMAGENET ACQUIRED
def get_image_paths(folder, test=False):
    image_paths = []
    if not test:
        for synset in os.listdir(folder):
            print(synset)
            # TODO: maybe remove {folder} as this will be part of static path ALSO CHANGE TO OS.PATH.JOIN
            subfolder = os.path.join(folder, synset, "images")
            for image_name in os.listdir(subfolder):
                image_paths.append(f"{subfolder}\\{image_name}")
    else:
        image_paths = []
        for image_name in os.listdir(folder):
            image_paths.append(f"{image_name}")

    return np.array(image_paths)


def get_images_batch(image_paths, start, end):
    batch = [Image.open(path) for path in image_paths[start:end]]
    return batch

def close_batch(batch):
    for image in batch:
        image.close()

def normalise(matrix):
    return matrix / np.linalg.norm(matrix, axis=0)

def save_object(object, filename):
    with open(filename, "wb") as object_file:
        pickle.dump(object, object_file)
    
def read_object(filename):
    with open(filename, 'rb') as object_file:
        return pickle.load(object_file)

