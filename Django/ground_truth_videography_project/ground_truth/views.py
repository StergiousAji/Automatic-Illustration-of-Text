from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader

from .forms import LinkForm, FileUploadForm

from videography_pipeline.audio_retriever import *
from videography_pipeline.audio_recogniser import *
from videography_pipeline.synced_lyrics_retriever import *

def home(request):
    src_folder = "videography_pipeline\\"
    link_form = LinkForm()
    file_upload_form = FileUploadForm()

    if request.method == "POST":
        if 'youtube_url' in request.POST:
            link_form = LinkForm(request.POST)

            if link_form.is_valid():
                clear_directories(src_folder)
                yt, audio_file, captions = download_yt(link_form.cleaned_data['youtube_url'], src_folder)
                title, artist = recognise_audio(yt, audio_file)

                if not captions:
                    synced_lyrics = get_synced_lyrics(title, artist, src_folder, yt.video_id)
                
        elif 'file' in request.POST:
            file_upload_form = FileUploadForm(request.POST, request.FILES)
            if file_upload_form.is_valid():
                print(file_upload_form.cleaned_data)
        
    context = { 
        'page_name': 'Home',
        'link_form': link_form,
        'file_upload_form': file_upload_form,
    }
    return render(request, 'ground_truth/home.html', context)

def about(request):
    return HttpResponse("About")

def collections(request):
    return HttpResponse("Collections")