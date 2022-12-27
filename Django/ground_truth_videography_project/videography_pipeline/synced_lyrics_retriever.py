# Source: https://github.com/fashni/MxLRC
from .mxlrc import Musixmatch, Song, get_lrc
import pylrc
import os

# TODO DELETE MAYBE???
MUSIXMATCH_ACCESS_TOKEN = "200501593b603a3fdc5c9b4a696389f6589dd988e5a1cf02dfdce1"

MUSIXMATCH_ACCESS_TOKEN = "2212262fac49706f69495b666eeb8b05c0b293b75997dd15e795af"
def get_synced_lyrics(title, artist, folder, filename=""):
    musixmatch = Musixmatch(MUSIXMATCH_ACCESS_TOKEN)
    song = Song(artist, title)

    transcript_path = os.path.join(folder, "transcript")
    success = get_lrc(musixmatch, song, transcript_path, filename)
    if success:
        with open(os.path.join(transcript_path, f"{filename}.lrc"), 'r', encoding='utf-8') as transcript:
            return transcript.read()