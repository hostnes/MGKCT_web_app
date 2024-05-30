from __future__ import absolute_import, unicode_literals
import os
import django
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')
django.setup()

app = Celery('server')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.broker_url = 'redis://redis:6379/0'
app.conf.result_backend = 'redis://redis:6379/0'

app.conf.accept_content = ['json']
app.conf.task_serializer = 'json'
app.conf.result_serializer = 'json'
app.conf.timezone = 'UTC'

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.autodiscover_tasks(['app'])

app.conf.beat_schedule = {
    'pars_students_html': {
        'task': 'app.tasks.pars_students_week',
        'schedule': crontab(minute='*/10'),
    },
    'pars_teachers_week': {
        'task': 'app.tasks.pars_teachers_week',
        'schedule': crontab(minute='*/10'),
    },
}

