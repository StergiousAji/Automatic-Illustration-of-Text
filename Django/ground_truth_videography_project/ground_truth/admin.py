from django.contrib import admin

from .models import GroundTruth, Chunk

# Register your models here.
admin.site.register(GroundTruth)
admin.site.register(Chunk)