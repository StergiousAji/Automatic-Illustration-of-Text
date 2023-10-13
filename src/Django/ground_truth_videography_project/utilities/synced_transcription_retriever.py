# Source: https://github.com/fashni/MxLRC
from .mxlrc import Musixmatch, Song, get_lrc
from pylrc.utilities import unpackTimecode
import pylrc
import os
import whisper

from config import MUSIXMATCH_ACCESS_TOKEN

def get_synced_lyrics(title, artist, folder, filename):
    musixmatch = Musixmatch(MUSIXMATCH_ACCESS_TOKEN)
    song = Song(artist, title)

    transcript_path = os.path.join(folder, "transcript")
    success = get_lrc(musixmatch, song, transcript_path, filename)
    if success:
        return read_transcript(os.path.join(transcript_path, f"{filename}.lrc"))

def read_transcript(filename):
    with open(filename, 'r', encoding="utf-8") as transcript:
        return transcript.read()

def seconds_to_time(total_seconds):
    minutes = int(total_seconds//60)
    seconds = total_seconds - minutes*60
    return f"{minutes}:{seconds:05.2f}"

def transcribe_audio(artist, title, folder, filename):
    model = whisper.load_model("small")
    transcription = model.transcribe(os.path.join(folder, "audio", f"{filename}.mp3"))

    lrc_string = f"[ar:{artist}]\n[ti:{title}]\n"
    for segment in transcription["segments"]:
        minutes, seconds = divmod(segment["end"], 60)
        lrc_string += f"[{int(minutes):02d}:{seconds:05.2f}] {segment['text']}\n"

    with open(os.path.join(folder, "transcript", f"{filename}.lrc"), 'w', encoding="utf-8") as transcript:
        transcript.write(lrc_string)
    
    return lrc_string

def get_transcript_length(transcript):
    lyrics = pylrc.parse(transcript)
    mins, secs, mills = unpackTimecode(f"[{lyrics.length}]")
    return sum([0, mins*60, secs, mills/1000])
