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
from videography_pipeline.Counter import Counter

SRC_FOLDER = "videography_pipeline\\"

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
                audio_path = save_file(audio_file, f"{SRC_FOLDER}audio")
                filename = audio_file.name.split('.')[0]
        
        if audio_path:
            title, artist = recognise_audio(audio_path, filename)

            if title and artist:
                synced_lyrics_path = get_synced_lyrics(title, artist, SRC_FOLDER, filename)

            audio = Audio(artist=artist, title=title, filename=filename)
            audio.save()
            return redirect(reverse('ground_truth:audio', kwargs={'audio_slug': audio.slug}))
        
    context = { 
        'link_form': link_form,
    }
    return render(request, 'ground_truth/home.html', context)


def audio(request, audio_slug):
    audio = Audio.objects.get(slug=audio_slug)

    lyrics = parse_lrc(f"{SRC_FOLDER}transcript\\{audio.filename}.lrc")
    lyrics_text = [lyric.text for lyric in lyrics]

    #TODO: MAKE CHUNKS FOR EACH LINE

    context = {
        'audio': audio,
        'transcript': lyrics_text,
        'coverart_colour': f"rgba{get_coverart_colour(audio.filename, SRC_FOLDER)}",
        'value': 0,
        'counter': Counter(),
    }
    return render(request, 'ground_truth/audio.html', context)


def chunk(request, audio_slug, chunk_slug):
    chunk = Chunk.objects.filter(audio__slug=audio_slug)
    print(chunk)

    context = {
        'chunk': chunk,
    }

    return render(request, 'ground_truth/chunk.html', context)


def about(request):
    return render(request, 'ground_truth/about.html')


def collections(request):
    return render(request, 'ground_truth/collections.html')