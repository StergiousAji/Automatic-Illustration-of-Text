from django.db import models
from django.template.defaultfilters import slugify
import json

class Audio(models.Model):
    artist = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    filename = models.CharField(max_length=50)
    transcript = models.TextField(blank=True, null=True)
    coverart_colour = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    # TODO: HOLD GROUND TRUTH DATA HERE
    
    def save(self, *args, **kwargs):
        self.slug = f"{slugify(self.artist)}-{slugify(self.title)}"
        # Delete any existing records of the same track.
        Audio.objects.filter(slug=self.slug).delete()
        super(Audio, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.artist} - {self.title}"
    
    class Meta:
        verbose_name_plural = 'Audio Tracks'

class Chunk(models.Model):
    index = models.IntegerField(unique=True, blank=True)
    text = models.CharField(max_length=200)
    audio = models.ForeignKey(Audio, on_delete=models.CASCADE, default=1)
    start_time = models.FloatField()
    end_time = models.FloatField()
    _image_ids = models.CharField(max_length=500)
    _selected_image_ids = models.CharField(max_length=500)
    slug = models.SlugField()

    @property
    def image_ids(self):
        return json.loads(self._image_ids)
    
    @image_ids.setter
    def image_ids(self, value):
        self._image_ids = json.dumps(value)
        print(self._image_ids)

    @property
    def selected_image_ids(self):
        return json.loads(self._selected_image_ids)
    
    @selected_image_ids.setter
    def selected_image_ids(self, value):
        self._selected_image_ids = json.dumps(value)

    def save(self, *args, **kwargs):
        self.slug = f"chunk-{slugify(self.index)}"
        # Delete any existing records of the same chunk.
        Chunk.objects.filter(index=self.index).delete()
        super(Chunk, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.audio} | Chunk {self.index}"
    
    class Meta: 
        verbose_name_plural = 'Chunks'