import os
from django.conf import settings
from requests.sessions import Request
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weatherpy.settings')

app = Celery('weatherpy')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Schedule tasks
app.conf.beat_schedule = {
    'run-every-30-minutes': {
        'task' : 'send_weather_report_email_task',
        'schedule' : crontab(minute='*/30'),
    }
}


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')