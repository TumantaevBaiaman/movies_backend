import uuid

from django.db import models

from apps.movies.models import Movie
from apps.users.models import User


class Favorite(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    movies = models.ManyToManyField(Movie)

    def add_to_favorites(self, movie):
        self.movies.add(movie)

    def remove_from_favorites(self, movie):
        self.movies.remove(movie)


