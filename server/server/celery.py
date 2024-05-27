
from __future__ import absolute_import, unicode_literals
import os
import django
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

print(os.path)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')

app = Celery('server')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.broker_url = settings.CELERY_BROKER_URL

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.autodiscover_tasks(['app'])

django.setup()

app.conf.timezone = settings.TIME_ZONE

app.conf.beat_schedule = {
    'pars_students_html': {
        'task': 'app.tasks.pars_students_html',
        'schedule': crontab(minute='*/10'),
    },
    'pars_teachers_week': {
        'task': 'app.tasks.pars_teachers_week',
        'schedule': crontab(minute='*/10'),
    },
}