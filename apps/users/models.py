from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    username = models.CharField("Имя пользователя", max_length=255)

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


class Subscription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def end_subscription(self):
        self.ended_at = timezone.now()
        self.active = False
        self.save()

    class Meta:
        verbose_name = "подписька"
        verbose_name_plural = "подписька"

    def __str__(self) -> str:
        return f"{self.user} {self.subscribed_at}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        user = self.user
        message = f'Вы успешно оформили подписку типа. Проверьте новинки на сайте!'
        notification = Notification.objects.create(message=message, notification_type=6, object_id=self.id)
        notification.users.set([user])


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        (1, "movie"),
        (2, "series"),
        (3, "season"),
        (4, "series_video"),
        (5, "other"),
        (6, "subscription")
    ]

    users = models.ManyToManyField(User, related_name='notifications')
    message = models.TextField()

    notification_type = models.IntegerField(choices=NOTIFICATION_TYPES)
    object_id = models.UUIDField()

    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-id",)

    def read_notification(self, user):
        self.users.remove(user)
