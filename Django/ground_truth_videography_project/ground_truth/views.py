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
from videography_pipeline.synced_lyrics_retriever import get_synced_lyrics, read_transcript, seconds_to_time
from videography_pipeline.image_retriever import CLIP, index_image_paths
from videography_pipeline.videography import build_video

import os
import pylrc
import numpy as np
import json


SRC_FOLDER = "videography_pipeline"
IMAGE_PATHS = np.delete(index_image_paths(os.path.relpath(settings.IMAGE_DATASET_DIR)), settings.EXCLUDE)
IMAGE_VECTOR_PATH = os.path.join(SRC_FOLDER, "image_vectors", "imagenet-1k-vecs-FILTERED.npy")

clip = CLIP(IMAGE_PATHS, IMAGE_VECTOR_PATH)

def home(request):
    link_form = LinkForm()
    audio_path = None
    filename = None
    transcript = None
    music = True

    if request.method == "POST":
        clear_directories(["audio", "transcript"], SRC_FOLDER)

        if 'youtube_url' in request.POST:
            link_form = LinkForm(request.POST)

            if link_form.is_valid():
                yt, audio_path, transcript = download_yt(link_form.cleaned_data['youtube_url'], SRC_FOLDER) 
                filename = yt.video_id
        
        elif 'audio_file' in request.FILES:
            audio_file = request.FILES['audio_file']
            # Validate the file is of audio format
            if 'audio' in audio_file.content_type:
                audio_path = save_file(audio_file, os.path.join(SRC_FOLDER, 'audio'))
                filename = audio_file.name.split('.')[0]
        
        if audio_path:
            title, artist = recognise_audio(audio_path, filename)
            coverart_colour = f"rgba{get_coverart_colour(filename, SRC_FOLDER)}"

            if title and artist and not transcript:
                transcript = get_synced_lyrics(title, artist, SRC_FOLDER, filename)
            elif not title and not artist:
                title = yt.title
                artist = yt.author
                music = False
            
            audio = Audio(music=music, artist=artist, title=title, filename=filename, transcript=transcript, coverart_colour=coverart_colour, _ground_truth="null")
            audio.save(True)
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
                    end_time=lyrics[i+1].time, _image_ids="[]", _selected_ids="[]")
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

    print(len(clip.image_paths))

    if chunk.image_ids == []:
        print("Performing query...")
        chunk.image_ids = clip.query_prompt(chunk.text)
        chunk.save()

    if request.method == "POST":
        post = request.POST.dict()

        chunk.selected_ids = [int(k) for k in post.keys() if k.isdigit()]
        chunk.save()

        redirect_chunk = chunk.slug
        if 'finish' in post:
            ground_truth = {
                'id': audio.filename,
                'artist': audio.artist,
                'title': audio.title,
            }

            chunks = []
            for c in Chunk.objects.filter(audio__slug=audio_slug):
                selected_image_paths = list(clip.image_paths[np.array(c.image_ids)[c.selected_ids]]) if c.selected_ids != [] else []
                print(c.selected_ids)
                print(selected_image_paths)
                chunks.append({
                    'index': c.index,
                    'text': c.text,
                    'start_time': c.start_time,
                    'end_time': c.end_time,
                    'selected_image_paths': selected_image_paths,
                })
            
            ground_truth['chunks'] = chunks

            audio.ground_truth = ground_truth
            audio.save(False)

            with open(os.path.join(SRC_FOLDER, "ground_truth", f"{audio.filename}.json"), "w", encoding='utf-8') as gt_json:
                json.dump(ground_truth, gt_json, indent=4, ensure_ascii=False)
            
            return redirect(reverse('ground_truth:ground-truth', kwargs={'audio_slug': audio.slug}))
        elif 'previous' in post:
            redirect_chunk = f"chunk-{chunk.index - 1}"
        elif 'next' in post:
            redirect_chunk = f"chunk-{chunk.index + 1}"
        
        return redirect(reverse('ground_truth:chunk', kwargs={'audio_slug': audio.slug, 'chunk_slug': redirect_chunk}))

    context = {
        'audio': audio,
        'chunk': chunk,
        'chunks': Chunk.objects.filter(audio__slug=audio_slug),
        'image_paths': clip.image_paths[chunk.image_ids],
        "start_time": seconds_to_time(chunk.start_time),
        "end_time": seconds_to_time(chunk.end_time)
    }
    return render(request, 'ground_truth/chunk.html', context)


def video(request, audio_slug):
    audio = Audio.objects.get(slug=audio_slug)
    
    video_path = os.path.join(SRC_FOLDER, "video", f"{audio.filename}.mp4")
    audio_path = os.path.join(SRC_FOLDER, "audio", f"{audio.filename}.mp3")

    if not os.path.exists(video_path) and os.path.exists(audio_path):
        chunks = Chunk.objects.filter(audio__slug=audio_slug).order_by("id")

        print("Building Video...")
        build_video(chunks, clip, audio_path, video_path)

    context = {
        'audio': audio,
        'video_exists': os.path.exists(video_path),
    }
    return render(request, 'ground_truth/video.html', context)


def ground_truth(request, audio_slug):
    return render(request, 'ground_truth/ground_truth.html', {'audio': Audio.objects.get(slug=audio_slug)})


def about(request):
    return render(request, 'ground_truth/about.html')


def collections(request):
    return render(request, 'ground_truth/collections.html', {'audio_tracks': Audio.objects.all()})