from django.db import models

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