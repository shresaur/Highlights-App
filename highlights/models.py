from django.db import models

# Create your models here.


class VideoList(models.Model):
    title = models.CharField(max_length=200)
    link = models.CharField(max_length=100)
    image = models.CharField(max_length=50)
    active = models.CharField(max_length=1)
    objects = models.Manager()

    def __str__(self):
        return self.title
