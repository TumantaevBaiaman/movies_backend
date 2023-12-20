import uuid

from django.db import models


class Director(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    name = models.CharField(max_length=255, unique=True)
    photo = models.ImageField(upload_to="actor")

    class Meta:
        verbose_name = "Режиссер"
        verbose_name_plural = "Режиссеры"

    def __str__(self):
        return f"{self.name}"
