from django.db import models

import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    username = models.CharField("Имя пользователя", max_length=255)
    phone = models.CharField("Номер телефона", max_length=30, unique=True, null=True, blank=True)

    is_activ = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)
    email_verify = models.BooleanField(default=False)

    confirmation_code = models.CharField(max_length=6, blank=True, null=True)
    confirmation_code_created_at = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ("username",)

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

    def __str__(self) -> str:
        return f"Username: {self.username}"
