from celery import shared_task
from datetime import timedelta
from django.utils import timezone
from django.core.mail import send_mail
from .models import Subscription
from apps.users.models import Subscription


@shared_task
def end_subscription_task(subscription_id):
    subscription = Subscription.objects.get(id=subscription_id)
    subscription.end_subscription()
