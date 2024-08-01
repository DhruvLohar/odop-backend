from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'odop_backend.settings')

app = Celery('odop_backend')  
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_connection_retry_on_startup = True

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f"[CELERY REQUEST] {self.request!r}")