from django.contrib.contenttypes.models import ContentType

from apps.users.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from apps.movies.models import Movie
from apps.users.models import Notification


@receiver(post_save, sender=Movie)
def mark_notification_as_read(sender, instance, created, **kwargs):
    if created:
        # Получаем пользователей, которые еще не прочитали уведомление
        users_to_notify = User.objects.all()

        message = f'Фильм "{instance.title}" был добавлен. Проверьте новинки на сайте!'

        # Создаем уведомление для каждого пользователя, исключая тех, кто его уже прочитал
        notification = Notification.objects.create(message=message, notification_type=1, object_id=instance.id)
        notification.users.set(users_to_notify)