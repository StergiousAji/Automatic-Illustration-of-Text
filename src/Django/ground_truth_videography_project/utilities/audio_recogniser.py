from ShazamAPI import Shazam
import urllib.parse
import requests
import os
from colorthief import ColorThief

def recognise_audio(filepath, filename, retries=1):
    with open(filepath, 'rb') as mp3_file:
        shazam = Shazam(mp3_file.read())
    
    title, artist, recognised = None, None, {}

    print("Recognising song...")
    while retries > 0:
        recognised = next(shazam.recognizeSong())[1]
        if "track" in recognised:
            break
        print(f"\u001b[31mTrying again...\u001b[0m")
        retries -= 1
    else:
        print(f"\u001b[31m\nUnable to recognise audio...\u001b[0m")
        return title, artist
        
    recognised = recognised["track"]

    title = urllib.parse.unquote_plus(recognised["urlparams"]["{tracktitle}"])
    artist = urllib.parse.unquote_plus(recognised["urlparams"]["{trackartist}"])

    print(f"\u001b[36m{artist} - {title}\u001b[0m")

    if "images" in recognised:
        imageURL = recognised["images"]["coverart"]
        parent_folder = os.path.split(os.path.split(filepath)[0])[0]
        print(parent_folder)
        save_coverart(imageURL, filename, parent_folder)
    
    return title, artist

def save_coverart(imageURL, filename, folder='.'):
    print("Downloading cover art...")
    with open(os.path.join(folder, "coverart", f"{filename}.png"), "wb") as cover_art_file:
        cover_art_file.write(requests.get(imageURL).content)
    
def get_coverart_colour(filename, folder='.'):
    filepath = os.path.join(folder, "coverart", f"{filename}.png")
    if os.path.exists(filepath):
        colourthief = ColorThief(filepath)
        # Add opacity to lighten colour
        return tuple(colourthief.get_color(quality=1)) + (0.97,)
    else:
        return (128, 128, 128)