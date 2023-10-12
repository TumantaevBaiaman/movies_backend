import uuid

from django.db import models

from apps.genres.models import Genre


class Movie(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    title = models.CharField(
        max_length=255, verbose_name="название фильма"
    )
    director = models.CharField(
        max_length=255, verbose_name="режиссер"
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
    movie_file = models.FileField(
        upload_to='movie_files',
        verbose_name="Фильм"
    )
    genres = models.ManyToManyField(
        Genre, verbose_name="жанры"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="дата создания записи"
    )

    is_activ = models.BooleanField(default=True)
    is_free = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"
