from ShazamAPI import Shazam
import urllib.parse
import requests

def save_cover_art(imageURL, filename):
    print("Downloading cover art...")
    with open(f"Images\\{filename}.jpg", "wb") as cover_art_file:
        cover_art_file.write(requests.get(imageURL).content)

def recognise_audio(filepath, yt):
    with open(filepath, 'rb') as mp3_file:
        shazam = Shazam(mp3_file.read())

    try:
        print("Recognising song...")
        recognised = next(shazam.recognizeSong())[1]["track"]

        title = urllib.parse.unquote_plus(recognised["urlparams"]["{tracktitle}"])
        artist = urllib.parse.unquote_plus(recognised["urlparams"]["{trackartist}"])
        imageURL = recognised["images"]["coverart"]

        print((title, artist))
        save_cover_art(imageURL, yt.video_id)

        return (title, artist)
    except Exception as ex:
        print(ex)