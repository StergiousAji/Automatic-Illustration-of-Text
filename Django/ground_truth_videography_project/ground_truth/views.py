from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.urls import reverse
from django.template.defaultfilters import slugify

from django.conf import settings

from .models import Audio
from .forms import LinkForm

from videography_pipeline.audio_retriever import *
from videography_pipeline.audio_recogniser import *
from videography_pipeline.synced_lyrics_retriever import *

src_folder = "videography_pipeline\\"

def home(request):
    link_form = LinkForm()
    audio_path = None
    captions = False
    filename = None

    if request.method == "POST":
        clear_directories(src_folder)

        if 'youtube_url' in request.POST:
            link_form = LinkForm(request.POST)

            if link_form.is_valid():
                yt, audio_path, captions = download_yt(link_form.cleaned_data['youtube_url'], src_folder) 
                filename = yt.video_id
        
        elif 'audio_file' in request.FILES:
            audio_file = request.FILES['audio_file']
            # Validate the file is of audio format
            if 'audio' in audio_file.content_type:
                audio_path = save_file(audio_file, f"{src_folder}audio")
                filename = audio_file.name.split('.')[0]
        
        if audio_path:
            title, artist = recognise_audio(audio_path, filename)

            if not captions and title and artist:
                synced_lyrics_path = get_synced_lyrics(title, artist, src_folder, filename)

            audio = Audio(artist=artist, title=title, filename=filename)
            audio.save()
            return redirect(reverse('ground_truth:result', kwargs={'audio_slug': audio.slug}))
        
    context = { 
        'page_name': 'Home',
        'link_form': link_form,
    }
    return render(request, 'ground_truth/home.html', context)


def result(request, audio_slug):
    audio = Audio.objects.get(slug=audio_slug)

    lyrics = parse_lrc(f"{src_folder}transcript\\{audio.filename}.lrc")
    lyrics_text = [lyric.text for lyric in lyrics]

    context = {
        'audio': audio,
        'text': lyrics_text,
        'coverart_colour': "#744242",
    }
    return render(request, 'ground_truth/result.html', context)

def about(request):
    return HttpResponse("About")

def collections(request):
    return HttpResponse("Collections")