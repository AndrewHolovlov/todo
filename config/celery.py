import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')

app = Celery('todo')
app.config_from_object('django.conf:settings')

app.autodiscover_tasks()



