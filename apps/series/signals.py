from django.contrib.contenttypes.models import ContentType

from apps.users.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

from apps.series.models import Series, Season, SeriesVideo
from apps.users.models import Notification


@receiver(post_save, sender=Series)
def create_series(sender, instance, created, **kwargs):
    if created:
        users_to_notify = User.objects.all()

        message = f'Сериал "{instance.title}" был добавлен. Проверьте новинки на сайте!'

        notification = Notification.objects.create(message=message, notification_type=2, object_id=instance.id)
        notification.users.set(users_to_notify)


@receiver(post_save, sender=Season)
def create_season(sender, instance, created, **kwargs):
    if created:
        users_to_notify = User.objects.all()

        message = f'{instance.season} сезон сериала {instance.series.title} был добавлен. Проверьте новинки на сайте!'

        notification = Notification.objects.create(message=message, notification_type=3, object_id=instance.id)
        notification.users.set(users_to_notify)