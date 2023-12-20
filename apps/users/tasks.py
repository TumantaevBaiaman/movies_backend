from celery import shared_task
from django.utils import timezone
from apps.users.models import Subscription


@shared_task
def deactivate_expired_subscriptions():
    expired_subscriptions = Subscription.objects.all()
    expired_subscriptions.update(active=False)
