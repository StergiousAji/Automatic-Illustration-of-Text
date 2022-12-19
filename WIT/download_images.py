import pandas as pd
import requests
from PIL import Image
import os, shutil

def download_images(filename="wit_1_percent.tsv"):
    wit = pd.read_csv(filename, sep="\t")
    # Filter only English
    wit = wit[wit["language"] == "en"].reset_index(drop=True)
    
    headers ={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
    }

    for i, image in enumerate(wit["image_url"]):
        filename = f"WIT_Images\\{i}.png"
        if not os.path.exists(filename):
            with open(filename, "wb") as image_file:
                image_file.write(requests.get(image, headers=headers).content)

            print(f"Downloading image {i}...")
            try:
                with Image.open(filename) as img:
                    width, height = img.size
                    img = img.resize((width//5, height//5), Image.ANTIALIAS)
                    img.save(filename, optimize=True, quality=95)
            except Exception as ex:
                print(ex)

download_images()