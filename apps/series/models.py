import uuid

from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from apps.actors.models import Actor
from apps.director.models import Director
from apps.genres.models import Genre


class Series(models.Model):
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
    poster = models.ImageField(
        blank=True, null=True, upload_to='poster', verbose_name="постер"
    )
    horizontal_poster = models.ImageField(
        blank=True, null=True, upload_to='horizontal-poster', verbose_name="горизонтальный постер"
    )
    release_date = models.DateField(
        "дата выпуска"
    )
    genres = models.ManyToManyField(
        Genre, verbose_name="жанры"
    )
    actors = models.ManyToManyField(
        Actor, verbose_name="актеры"
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

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Сериал"
        verbose_name_plural = "Сериалы"


class Season(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    series = models.ForeignKey(Series, on_delete=models.CASCADE)
    season = models.IntegerField(default=1)
    release_date = models.DateField(
        "дата выпуска"
    )

    is_activ = models.BooleanField(default=True)
    is_free = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.season}"

    class Meta:
        verbose_name = "Сезон"
        verbose_name_plural = "Сезоны"


class SeriesVideo(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    series = models.IntegerField(default=1)
    series_video = models.FileField(
        upload_to="series-video",
        validators=[FileExtensionValidator(allowed_extensions=['mp4'])]
    )
    series_video_1080 = models.FileField(
        upload_to="series-video",
        validators=[FileExtensionValidator(allowed_extensions=['mp4'])],
        blank=True,
        null=True
    )
    release_date = models.DateField(
        "дата выпуска"
    )

    # Поле для связи с Series или Season
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    content_object = GenericForeignKey('content_type', 'object_id')

    is_activ = models.BooleanField(default=True)
    is_free = models.BooleanField(default=False)

    views = models.PositiveIntegerField(default=0, verbose_name="количество просмотров")

    def increment_views(self):
        self.views += 1
        self.save()

    class Meta:
        verbose_name = "Сериал видео"
        verbose_name_plural = "Сериалы видео"




