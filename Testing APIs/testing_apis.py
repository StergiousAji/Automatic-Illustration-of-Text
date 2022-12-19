from lyricsgenius import Genius
from ShazamAPI import Shazam
# Source: https://github.com/fashni/MxLRC
from mxlrc import Musixmatch, Song, get_lrc
import re
import os
import shutil
import urllib.parse
import requests
import sys

import pytube
from html import unescape
import xml.etree.ElementTree as ElementTree

# Bug in pytube internal xml -> srt conversion. Modified to updated YouTube's xml format.
# Source: https://stackoverflow.com/questions/68780808/xml-to-srt-conversion-not-working-after-installing-pytube.
def xml_to_srt_captions(xml_captions: str) -> str:
        """Convert xml caption tracks to "SubRip Subtitle (srt)". MODIFIED

        :param str xml_captions:
            XML formatted caption tracks.
        """
        segments = []
        root = ElementTree.fromstring(xml_captions)
        for i, child in enumerate(list(root.findall('body/p'))):
            text = ''.join(child.itertext()).strip()
            if not text:
                continue
            caption = unescape(text.replace("\n", " ").replace("  ", " "),)
            try:
                duration = float(child.attrib["d"])
            except KeyError:
                duration = 0.0
            start = float(child.attrib["t"])
            end = start + duration
            sequence_number = i + 1  # convert from 0-indexed to 1.
            line = "{seq}\n{start} --> {end}\n{text}\n".format(
                seq=sequence_number,
                start=pytube.Caption.float_to_srt_time_format(start),
                end=pytube.Caption.float_to_srt_time_format(end),
                text=caption,
            )
            segments.append(line)
        return "\n".join(segments).strip()

# GENIUS
GENIUS_ACCESS_TOKEN = "fhJghXLRdI2UDMZajTHSZnitVnAyki9Az2ajdgDC0l0Gcic5dJOK3haId8GJWruT"
def extractLyrics(artist_name, song_name):
    genius = Genius(GENIUS_ACCESS_TOKEN, verbose=False, remove_section_headers=True)

    artist = genius.search_artist(artist_name, max_songs=1, sort="title", include_features=True)
    song = artist.song(song_name)
    lyrics = song.lyrics
    # Take everything after the first new line
    lyrics = lyrics[lyrics.find('\n'):]

    # Filter out the ending line by Genius
    lyrics = re.sub(r"You might also like[a-zA-Z0-9]*|[0-9]{1,2}(?:Embed)?", "", lyrics)

    return lyrics

MUSIXMATCH_ACCESS_TOKEN = "2203269256ff7abcb649269df00e14c833dbf4ddfb5b36a1aae8b0"
def get_synced_lyrics(artist, title, filename=""):
    musixmatch = Musixmatch(MUSIXMATCH_ACCESS_TOKEN)
    song = Song(artist, title)
    get_lrc(musixmatch, song, "Transcripts\\", filename)


# Clear directories
folders = ["Audio", "Images", "Transcripts"]
for f in folders:
    shutil.rmtree(f)
    os.mkdir(f)

# PYTUBE
yt = pytube.YouTube(sys.argv[1])
language = 'a.en'
if 'en' in yt.captions:
    language = 'en'

try:
    print(f"Grabbing {language} captions...")
    srt_captions = xml_to_srt_captions(yt.captions[language].xml_captions)

    with open(f"Transcripts\\{yt.video_id}.srt", 'w') as captions_file:
        captions_file.write(srt_captions)
except Exception as ex:
    print(ex)

print("Downloading audio...")
out_file = yt.streams.get_audio_only().download("Audio")
audio_file = f"Audio\\{yt.video_id}.mp3"
# Rename downloaded mp4 into mp3 to convert to audio file.
os.rename(os.path.relpath(out_file), audio_file)

# SHAZAM
mp3_file = open(audio_file, 'rb').read()

shazam = Shazam(mp3_file)

try:
    print("Recognising song...")
    recognised = next(shazam.recognizeSong())[1]["track"]

    title = urllib.parse.unquote_plus(recognised["urlparams"]["{tracktitle}"])
    artist = urllib.parse.unquote_plus(recognised["urlparams"]["{trackartist}"])
    imageURL = recognised["images"]["coverart"]

    print((title, artist))

    print("Downloading cover art...")
    with open(f"Images\\{yt.video_id}.jpg", "wb") as cover_art_file:
        cover_art_file.write(requests.get(imageURL).content)

    get_synced_lyrics(artist, title, yt.video_id)
        
    # -- Use as backup
    print("\nGenius:")
    print(extractLyrics(artist, title))
except Exception as ex:
    print(ex)

# try:
#     print("\n\nTry getting from shazam")
#     lyrics = recognised["sections"][1]["text"]
#     print("Shazam:\n")
#     for line in lyrics:
#         print(line)
# except Exception as ex:
#     print(ex)