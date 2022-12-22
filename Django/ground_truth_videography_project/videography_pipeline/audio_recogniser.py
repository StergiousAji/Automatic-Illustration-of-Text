from ShazamAPI import Shazam
import urllib.parse
import requests
import os

def recognise_audio(yt, filepath):
    with open(filepath, 'rb') as mp3_file:
        shazam = Shazam(mp3_file.read())

    try:
        print("Recognising song...")
        recognised = next(shazam.recognizeSong())[1]["track"]

        title = urllib.parse.unquote_plus(recognised["urlparams"]["{tracktitle}"])
        artist = urllib.parse.unquote_plus(recognised["urlparams"]["{trackartist}"])
        imageURL = recognised["images"]["coverart"]

        print(f"{artist} - {title}")
        parent_folder = os.path.split(os.path.split(filepath)[0])[0]
        save_coverart(imageURL, yt.video_id, parent_folder)

        return title, artist
    except Exception as ex:
        print(f"Error: {ex}")

def save_coverart(imageURL, filename, folder='.'):
    print("Downloading cover art...")
    with open(f"{folder}\\coverart\\{filename}.jpg", "wb") as cover_art_file:
        cover_art_file.write(requests.get(imageURL).content)