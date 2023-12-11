import uuid

from django.db import models

from apps.movies.models import Movie
from apps.series.models import Series, SeriesVideo
from apps.users.models import User


class WatchHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, null=True, blank=True, on_delete=models.CASCADE)
    series = models.ForeignKey(SeriesVideo, null=True, blank=True, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
