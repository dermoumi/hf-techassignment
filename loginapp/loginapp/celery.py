import os
from celery import Celery
from django.conf import settings

# Set the default Django settings module for `celery`
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'loginapp.settings')

app = Celery('loginapp')

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
