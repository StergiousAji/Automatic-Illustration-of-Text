from django.urls import path

from . import views

app_name = 'ground_truth'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('collections/', views.collections, name='collections'),
    path('<slug:audio_slug>/', views.audio, name='audio'),
    path('<slug:audio_slug>/<slug:chunk_slug>/', views.chunk, name='chunk'),
    path('<slug:audio_slug>/video', views.video, name='video'),
    path('<slug:audio_slug>/ground-truth', views.ground_truth, name='ground-truth'),
]