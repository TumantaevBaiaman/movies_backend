import uuid

from django.db import models

from apps.movies.models import Movie
from apps.series.models import SeriesVideo, Series
from apps.users.models import User


class Favorite(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    movies = models.ManyToManyField(Movie)
    series = models.ManyToManyField(Series)

    def add_to_favorites_movies(self, movie):
        self.movies.add(movie)

    def remove_from_favorites_movies(self, movie):
        self.movies.remove(movie)

    def add_to_favorites_series(self, series):
        self.series.add(series)

    def remove_from_favorites_series(self, series):
        self.series.remove(series)


