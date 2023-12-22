from django.db import models

# Create your models here.
# models.py
from django.conf import settings
from django.db import models


class Movie(models.Model):
    ml_id = models.IntegerField(
        "Movie Lense ID",
        default=0,
        blank=True,
    )
    title = models.CharField(
        "Movie Title",
        max_length=200,
        blank=True,
    )
    imdb_id = models.IntegerField(
        "IMDB ID",
        default=0,
        blank=True,
    )
    tags = models.TextField()
    cleaned_title = models.CharField(
        "Cleaned Movie Title",
        max_length=200,
        blank=True,
    )
