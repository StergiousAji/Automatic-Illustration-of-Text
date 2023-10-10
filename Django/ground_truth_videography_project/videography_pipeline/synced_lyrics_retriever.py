# Source: https://github.com/fashni/MxLRC
from .mxlrc import Musixmatch, Song, get_lrc
import pylrc
import os

# Insert MusixMatch Access Token here
MUSIXMATCH_ACCESS_TOKEN = None
def get_synced_lyrics(title, artist, folder, filename=""):
    musixmatch = Musixmatch(MUSIXMATCH_ACCESS_TOKEN)
    song = Song(artist, title)

    transcript_path = os.path.join(folder, "transcript")
    success = get_lrc(musixmatch, song, transcript_path, filename)
    if success:
        with open(os.path.join(transcript_path, f"{filename}.lrc"), 'r', encoding='utf-8') as transcript:
            return transcript.read()
