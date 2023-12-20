from django.db import models

import uuid

from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Actor(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    name = models.CharField(max_length=255, unique=True)
    photo = models.ImageField(upload_to="actor")

    class Meta:
        verbose_name = "Актер"
        verbose_name_plural = "Актеры"

    def __str__(self):
        return f"{self.name}"
