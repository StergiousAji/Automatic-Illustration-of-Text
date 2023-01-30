from django.contrib import admin

from .models import Audio, Chunk

# Register your models here.
admin.site.register(Audio)
admin.site.register(Chunk)