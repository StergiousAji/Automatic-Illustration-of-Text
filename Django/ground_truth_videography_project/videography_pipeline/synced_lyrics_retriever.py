# Source: https://github.com/fashni/MxLRC
from .mxlrc import Musixmatch, Song, get_lrc
from pylrc.utilities import unpackTimecode
import pylrc
import os

MUSIXMATCH_ACCESS_TOKEN = "2212262fac49706f69495b666eeb8b05c0b293b75997dd15e795af"
def get_synced_lyrics(title, artist, folder, filename=""):
    musixmatch = Musixmatch(MUSIXMATCH_ACCESS_TOKEN)
    song = Song(artist, title)

    transcript_path = os.path.join(folder, "transcript")
    success = get_lrc(musixmatch, song, transcript_path, filename)
    if success:
        return read_transcript(os.path.join(transcript_path, f"{filename}.lrc"))

def read_transcript(filename):
    with open(filename, 'r', encoding="utf-8") as transcript:
        return transcript.read()

def get_transcript_length(transcript):
    lyrics = pylrc.parse(transcript)
    mins, secs, mills = unpackTimecode(f"[{lyrics.length}]")
    return sum([0, mins*60, secs, mills/1000])
