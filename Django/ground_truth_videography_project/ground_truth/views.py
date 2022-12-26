from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.conf import settings

from .models import Audio, Chunk
from .forms import LinkForm

from videography_pipeline.audio_retriever import clear_directories, download_yt, save_file
from videography_pipeline.audio_recogniser import recognise_audio, get_coverart_colour
from videography_pipeline.synced_lyrics_retriever import get_synced_lyrics, parse_lrc
from videography_pipeline.image_retriever import CLIP, get_image_paths, save_object, read_object
from videography_pipeline.counter import Counter

import os, subprocess, pytube

SRC_FOLDER = "videography_pipeline"

# WEIRD SHIT HAPPENS WITH THIS
clip = CLIP(folder=os.path.relpath(settings.IMAGES_DATASET_DIR))

# download_yt("https://www.youtube.com/watch?v=_B6T8O15Ohk", SRC_FOLDER)

def download_audio(url):
    default_file = "downloads\\Video Not Available.mp4"
    out_file = default_file
    while os.path.relpath(out_file) == default_file:
        if os.path.exists(out_file):
            os.remove(out_file)
        ydl = pytube.YouTube(url)
        out_file = ydl.streams.get_audio_only().download(output_path="downloads")
    
    audio_file = f"{out_file.split('.')[0]}.mp3"
    subprocess.run(['ffmpeg', '-i', out_file, '-b:a', '192K', audio_file, '-hide_banner', '-loglevel', 'quiet'])
    os.remove(out_file)
    return audio_file

# pytube.YouTube("https://www.youtube.com/watch?v=6zf2dNLS-fs").streams.filter(progressive=True, file_extension='mp4').order_by('resolution')[-1].download()

def home(request):
    link_form = LinkForm()
    audio_path = None
    captions = False
    filename = None

    if request.method == "POST":
        clear_directories(SRC_FOLDER)

        if 'youtube_url' in request.POST:
            link_form = LinkForm(request.POST)

            if link_form.is_valid():
                yt, audio_path, captions = download_yt(link_form.cleaned_data['youtube_url'], SRC_FOLDER) 
                filename = yt.video_id
        
        elif 'audio_file' in request.FILES:
            audio_file = request.FILES['audio_file']
            # Validate the file is of audio format
            if 'audio' in audio_file.content_type:
                audio_path = save_file(audio_file, os.path.join(SRC_FOLDER, 'audio'))
                filename = audio_file.name.split('.')[0]
        
        if audio_path:
            title, artist = recognise_audio(audio_path, filename)

            if title and artist:
                get_synced_lyrics(title, artist, SRC_FOLDER, filename)

            audio = Audio(artist=artist, title=title, filename=filename, coverart_colour=f"rgba{get_coverart_colour(filename, SRC_FOLDER)}")
            audio.save()
            return redirect(reverse('ground_truth:audio', kwargs={'audio_slug': audio.slug}))
        
    context = { 
        'link_form': link_form,
    }
    return render(request, 'ground_truth/home.html', context)


def audio(request, audio_slug):
    audio = Audio.objects.get(slug=audio_slug)

    lyrics = parse_lrc(os.path.join(SRC_FOLDER, "transcript", f"{audio.filename}.lrc"))
    lyrics_text = [lyric.text for lyric in lyrics]

    chunks = []
    id = 1
    for i in range(len(lyrics) - 1):
        # Skip instrumental parts of the song
        if (lyrics[i].text == "♪"):
            continue
        
        lyric = lyrics[i]
        print(f"Chunk {id}: {lyric.text}")
        chunk = Chunk.objects.filter(index=id, audio__slug=audio.slug)

        if chunk.exists():
            print("Updating existing Chunk...")
            chunk.update(index=id, text=lyric.text, audio=audio, start_time=lyric.time, 
                end_time=lyrics[i+1].time)
            chunk = chunk[0]
        else:
            chunk = Chunk(index=id, text=lyric.text, audio_id=audio.id, start_time=lyric.time, 
                end_time=lyrics[i+1].time, _image_ids="[]", _selected_image_ids="[]")
            chunk.save()
        
        print(chunk)
        chunks.append(chunk)
        id += 1

    Audio.objects.filter(slug=audio.slug).update(chunks=len(chunks))

    context = {
        'audio': audio,
        'transcript': lyrics_text,
        'chunks': chunks,
    }
    return render(request, 'ground_truth/audio.html', context)


def chunk(request, audio_slug, chunk_slug):
    audio = Audio.objects.get(slug=audio_slug)
    chunk = Chunk.objects.get(slug=chunk_slug, audio__slug=audio_slug)
    print(chunk)

    image_vectors_path = os.path.join(SRC_FOLDER, "image_vectors", "tiny-imagenet-test_array.obj")
    if not os.path.exists(image_vectors_path):
        print("Processing images...")
        img_vectors = clip.process_images()
        save_object(img_vectors, image_vectors_path)
    else:
        img_vectors = read_object(image_vectors_path)

    if chunk.image_ids == []:
        print("Performing query...")
        chunk.image_ids = clip.query_prompt(chunk.text, img_vectors)
        chunk.save()
    
    next_slug = f"chunk-{chunk.index + 1}"

    context = {
        'audio': audio,
        'chunk': chunk,
        'image_paths': clip.image_paths[chunk.image_ids],
        'prev_slug': f'chunk-{chunk.index - 1}',
        'next_slug': next_slug,
    }

    return render(request, 'ground_truth/chunk.html', context)


def about(request):
    return render(request, 'ground_truth/about.html')


def collections(request):
    return render(request, 'ground_truth/collections.html')