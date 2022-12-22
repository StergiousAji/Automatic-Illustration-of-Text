import pytube
from html import unescape
import xml.etree.ElementTree as ElementTree
import os, shutil

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

def clear_directories(folder='.'):
    folders = ["audio", "coverart", "transcript"]
    for f in folders:
        path = f"{folder}\\{f}"
        shutil.rmtree(path)
        os.mkdir(path)

def download_yt(url, folder='.'):
    yt = pytube.YouTube(url)
    language = 'a.en'
    if 'en' in yt.captions:
        language = 'en'

    captions = False
    try:
        print(f"Try grabbing {language} captions...")
        srt_captions = xml_to_srt_captions(yt.captions[language].xml_captions)

        with open(f"{folder}\\transcript\\{yt.video_id}.srt", 'w') as captions_file:
            captions_file.write(srt_captions)
        captions = True
    except Exception as ex:
        print(f"Error: {ex}")

    print("Downloading audio...")
    out_file = yt.streams.get_audio_only().download("Audio")
    audio_file = f"{folder}\\audio\\{yt.video_id}.mp3"
    # Rename downloaded mp4 into mp3 to convert to audio file.
    os.rename(os.path.relpath(out_file), audio_file)

    return yt, audio_file, captions

# TODO Handle MP3 files raw