import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'logistic.settings')

app = Celery('logistic')
app.config_from_object('django.conf:settings', namespace='CELERY')
broker_connection_retry_on_startup = True
app.autodiscover_tasks()