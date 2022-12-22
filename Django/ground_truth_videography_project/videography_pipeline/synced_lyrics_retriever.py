# Source: https://github.com/fashni/MxLRC
from .mxlrc import Musixmatch, Song, get_lrc

MUSIXMATCH_ACCESS_TOKEN = "2203269256ff7abcb649269df00e14c833dbf4ddfb5b36a1aae8b0"
def get_synced_lyrics(title, artist, folder, filename=""):
    musixmatch = Musixmatch(MUSIXMATCH_ACCESS_TOKEN)
    song = Song(artist, title)
    return get_lrc(musixmatch, song, f"{folder}\\transcript\\", filename)