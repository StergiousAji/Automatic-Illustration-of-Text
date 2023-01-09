import pytube
from html import unescape
import xml.etree.ElementTree as ElementTree
import os, shutil

def clear_directories(subfolders, folder='.'):
    for f in subfolders:
        path = os.path.join(folder, f)
        shutil.rmtree(path)
        os.mkdir(path)

def download_yt(url, folder='.'):
    yt = pytube.YouTube(url, use_oauth=True)
    captions = 'en' if 'en' in yt.captions else ('a.en' if 'a.en' in yt.captions else None)

    if captions:
        print(f"Grabbing {captions} captions...")
        srt_captions = xml_to_srt_captions(yt.captions[captions].xml_captions)

        with open(os.path.join(folder, "transcript", f"{yt.video_id}.srt"), 'w', encoding="utf-8") as captions_file:
            captions_file.write(srt_captions)

    print("Downloading audio...")
    audio_folder = os.path.join(folder, "audio")

    default_file = "Video Not Available.mp4"
    out_file = default_file
    while os.path.relpath(out_file) == default_file:
        if os.path.exists(out_file):
            os.remove(out_file)
        out_file = yt.streams.get_audio_only().download()

    audio_file = os.path.join(audio_folder, f"{yt.video_id}.mp3")
    # Rename downloaded mp4 into mp3 to convert to audio file.
    os.rename(os.path.relpath(out_file), audio_file)

    return yt, audio_file, captions

# Handle audio file uploads
def save_file(file, folder):
    path = os.path.join(folder, file.name)
    with open(path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    
    return path


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