# celery_system/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Установка переменной окружения 'DJANGO_SETTINGS_MODULE'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movies_backend.settings')

app = Celery('movies_backend')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()