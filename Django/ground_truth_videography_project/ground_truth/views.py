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
from videography_pipeline.synced_lyrics_retriever import get_synced_lyrics, read_transcript
from videography_pipeline.image_retriever import CLIP, index_image_paths
from videography_pipeline.videography import build_video

import os
import pylrc
import numpy as np


SRC_FOLDER = "videography_pipeline"
IMAGE_PATHS = np.delete(index_image_paths(os.path.relpath(settings.IMAGE_DATASET_DIR)), settings.EXCLUDE)
IMAGE_VECTOR_PATH = os.path.join(SRC_FOLDER, "image_vectors", "imagenet-1k-vecs-FILTERED.npy")

clip = CLIP(image_paths=IMAGE_PATHS)

def home(request):
    link_form = LinkForm()
    audio_path = None
    captions = None
    filename = None
    transcript = None

    if request.method == "POST":
        clear_directories(["audio", "transcript"], SRC_FOLDER)

        if 'youtube_url' in request.POST:
            link_form = LinkForm(request.POST)

            if link_form.is_valid():
                # TODO: VALIDATE URL
                yt, audio_path, captions = download_yt(link_form.cleaned_data['youtube_url'], SRC_FOLDER) 
                filename = yt.video_id

                if captions:
                    transcript = read_transcript(os.path.join(SRC_FOLDER, "transcript", f"{filename}.srt"))
        
        elif 'audio_file' in request.FILES:
            audio_file = request.FILES['audio_file']
            # Validate the file is of audio format
            if 'audio' in audio_file.content_type:
                audio_path = save_file(audio_file, os.path.join(SRC_FOLDER, 'audio'))
                filename = audio_file.name.split('.')[0]
        
        if audio_path:
            title, artist = recognise_audio(audio_path, filename)
            coverart_colour = f"rgba{get_coverart_colour(filename, SRC_FOLDER)}"

            if title and artist:
                transcript = get_synced_lyrics(title, artist, SRC_FOLDER, filename)
                
                audio = Audio(artist=artist, title=title, filename=filename, transcript=transcript, coverart_colour=coverart_colour)
            else:
                audio = Audio(filename=filename, transcript=transcript, coverart_colour=coverart_colour)
            
            audio.save()
            return redirect(reverse('ground_truth:audio', kwargs={'audio_slug': audio.slug}))
        
    context = { 
        'link_form': link_form, 
    }
    return render(request, 'ground_truth/home.html', context)


def audio(request, audio_slug):
    audio = Audio.objects.get(slug=audio_slug)
    chunks = []

    instrumental = False

    if audio.transcript:
        instrumental = "♪ Instrumental ♪" in audio.transcript

        lyrics = pylrc.parse(audio.transcript)
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
                chunk.update(text=lyric.text, audio_id=audio.id, start_time=lyric.time, 
                    end_time=lyrics[i+1].time)
                chunk = chunk[0]
            else:
                chunk = Chunk(index=id, text=lyric.text, audio_id=audio.id, start_time=lyric.time, 
                    end_time=lyrics[i+1].time, _image_ids="[]", _selected_image_ids="[]")
                chunk.save()

            chunks.append(chunk)
            id += 1

    context = {
        'audio': audio,
        'chunks': chunks,
        'instrumental': instrumental,
    }
    return render(request, 'ground_truth/audio.html', context)


def chunk(request, audio_slug, chunk_slug):
    audio = Audio.objects.get(slug=audio_slug)
    chunk = Chunk.objects.get(slug=chunk_slug, audio__slug=audio_slug)
    print(chunk)

    chunks = Chunk.objects.filter(audio__slug=audio_slug)

    print(len(clip.image_paths))

    if clip.image_vectors is None:
        clip.load_image_vectors(IMAGE_VECTOR_PATH)

    if chunk.image_ids == []:
        print("Performing query...")
        chunk.image_ids = clip.query_prompt(chunk.text)
        chunk.save()

    context = {
        'audio': audio,
        'chunk': chunk,
        'chunks': chunks,
        'image_paths': clip.image_paths[chunk.image_ids],
        'prev_slug': f"chunk-{chunk.index - 1}",
        'next_slug': f"chunk-{chunk.index + 1}",
    }
    return render(request, 'ground_truth/chunk.html', context)


def video(request, audio_slug):
    audio = Audio.objects.get(slug=audio_slug)
    
    video_path = os.path.join(SRC_FOLDER, "video", f"{audio.filename}.mp4")
    audio_path = os.path.join(SRC_FOLDER, "audio", f"{audio.filename}.mp3")

    if not os.path.exists(video_path) and os.path.exists(audio_path):
        if clip.image_vectors is None:
            clip.load_image_vectors(IMAGE_VECTOR_PATH)

        chunks = Chunk.objects.filter(audio__slug=audio_slug).order_by("id")

        print("Building Video...")
        build_video(chunks, clip, audio_path, video_path)

    context = {
        'audio': audio,
        'audio_exists': os.path.exists(audio_path),
    }
    return render(request, 'ground_truth/video.html', context)


def ground_truth(request, audio_slug):
    audio = Audio.objects.get(slug=audio_slug)
    chunks = Chunk.objects.filter(audio__slug=audio_slug)

    context = {
        'audio': audio,
    }
    return render(request, 'ground_truth/ground_truth.html', context)


def about(request):
    return render(request, 'ground_truth/about.html')


def collections(request):
    audio_tracks = Audio.objects.all()

    context = {
        'audio_tracks': audio_tracks,
    }
    return render(request, 'ground_truth/collections.html', context)