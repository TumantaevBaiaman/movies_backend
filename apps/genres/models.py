import uuid

from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Genre(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    name = models.CharField(max_length=255, unique=True)
    icon = models.ImageField(blank=True, null=True, upload_to='genre_icon', verbose_name="иконка")

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"