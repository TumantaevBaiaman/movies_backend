import uuid

from django.core.validators import FileExtensionValidator
from django.db import models

from apps.actors.models import Actor
from apps.director.models import Director
from apps.genres.models import Genre


class Movie(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    title = models.CharField(
        max_length=255, verbose_name="название фильма"
    )
    directors = models.ManyToManyField(
        Director, verbose_name="режиссеры"
    )
    description = models.TextField(
        verbose_name="описание"
    )
    release_date = models.DateField(
        "дата выпуска"
    )
    poster = models.ImageField(
        blank=True, null=True, upload_to='poster', verbose_name="постер"
    )
    horizontal_poster = models.ImageField(
        blank=True, null=True, upload_to='horizontal-poster', verbose_name="горизонтальный постер"
    )
    genres = models.ManyToManyField(
        Genre, verbose_name="жанры"
    )
    actors = models.ManyToManyField(
        Actor, verbose_name="актеры"
    )
    movie = models.FileField(
        upload_to="origin-movie",
        validators=[FileExtensionValidator(allowed_extensions=['mp4'])]
    )
    trailer = models.FileField(
        upload_to="trailer",
        validators=[FileExtensionValidator(allowed_extensions=['mp4'])],
        blank=True, null=True
    )
    age_limit = models.IntegerField(default=2, blank=True, null=True)
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="дата создания записи"
    )

    moon = models.BooleanField(default=False)
    is_activ = models.BooleanField(default=True)
    is_free = models.BooleanField(default=False)

    views = models.PositiveIntegerField(default=0, verbose_name="количество просмотров")

    def increment_views(self):
        self.views += 1
        self.save()

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"


class FormatMovie(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    quality = models.CharField(max_length=255)
    movie_file = models.FileField(
        upload_to="format-movie",
        validators=[FileExtensionValidator(allowed_extensions=['mp4'])]
    )