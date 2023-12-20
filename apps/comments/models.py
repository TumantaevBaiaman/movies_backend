import uuid

from django.core.validators import MaxValueValidator
from django.db import models

from apps.movies.models import Movie
from apps.series.models import SeriesVideo, Series
from apps.users.models import User


class Comment(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=5, validators=[MaxValueValidator(10)])
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Комментария"
        verbose_name_plural = "Коментарии"
        ordering = ['-created_at']


class CommentSeries(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(default=5, validators=[MaxValueValidator(10)])
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Комментария для сериала"
        verbose_name_plural = "Коментарии для сериалов"
        ordering = ['-created_at']
