# Source: https://github.com/fashni/MxLRC
from .mxlrc import Musixmatch, Song, get_lrc
import pylrc
import os

MUSIXMATCH_ACCESS_TOKEN = "2212262fac49706f69495b666eeb8b05c0b293b75997dd15e795af"
def get_synced_lyrics(title, artist, folder, filename=""):
    musixmatch = Musixmatch(MUSIXMATCH_ACCESS_TOKEN)
    song = Song(artist, title)

    get_lrc(musixmatch, song, os.path.join(folder, "transcript"), filename)

def parse_lrc(transcript_path):
    with open(transcript_path, 'r', encoding='utf-8') as transcript:
        lrc = ''.join(transcript.readlines())
    
    return pylrc.parse(lrc)
