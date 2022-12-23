from django.db import models
from django.template.defaultfilters import slugify

class Audio(models.Model):
    artist = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    filename = models.CharField(max_length=50)
    slug = models.SlugField(unique=False)

    class Meta:
        verbose_name_plural = 'Audio Tracks'
    
    def save(self, *args, **kwargs):
        self.slug = f"{slugify(self.artist)}-{slugify(self.title)}"
        # Delete any existing records of the same track.
        Audio.objects.filter(slug=self.slug).delete()
        super(Audio, self).save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.artist} - {self.title}"

# Maybe not needed!
class GroundTruth(models.Model):
    name = models.CharField(max_length=50)
    start_time = models.TimeField()
    duration = models.TimeField()

    def __str__(self):
        return self.name

class Chunk(models.Model):
    index = models.IntegerField()
    text = models.CharField(max_length=200)
    ground_truth = models.ForeignKey(GroundTruth, on_delete=models.CASCADE)
    start_time = models.TimeField()
    duration = models.TimeField()
    image = models.ImageField()

    def __str__(self):
        return self.index