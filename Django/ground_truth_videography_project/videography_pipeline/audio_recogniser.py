from ShazamAPI import Shazam
import urllib.parse
import requests
import os

def recognise_audio(filepath, filename):
    with open(filepath, 'rb') as mp3_file:
        shazam = Shazam(mp3_file.read())
    
    title, artist = None, None

    try:
        print("Recognising song...")
        recognised = next(shazam.recognizeSong())[1]["track"]

        title = urllib.parse.unquote_plus(recognised["urlparams"]["{tracktitle}"])
        artist = urllib.parse.unquote_plus(recognised["urlparams"]["{trackartist}"])
        imageURL = recognised["images"]["coverart"]

        print(f"\u001b[36m{artist} - {title}\u001b[0m")
        parent_folder = os.path.split(os.path.split(filepath)[0])[0]
        save_coverart(imageURL, filename, parent_folder)
    except Exception as ex:
        print(f"\u001b[31m{type(ex).__name__}: {ex.args}\u001b[0m")
    
    return title, artist


def save_coverart(imageURL, filename, folder='.'):
    print("Downloading cover art...")
    with open(f"{folder}\\coverart\\{filename}.png", "wb") as cover_art_file:
        cover_art_file.write(requests.get(imageURL).content)