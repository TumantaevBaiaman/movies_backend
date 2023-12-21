from celery import shared_task
from django.utils import timezone
from apps.users.models import Subscription


@shared_task
def deactivate_expired_subscriptions():
    current_time = timezone.now()
    expired_subscriptions = Subscription.objects.filter(ended_at__lte=current_time, active=True)

    for subscription in expired_subscriptions:
        subscription.active = False
        subscription.save()
