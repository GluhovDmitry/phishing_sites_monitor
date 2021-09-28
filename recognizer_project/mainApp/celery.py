import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HotelLabIO.settings')

app = Celery('mainApp')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.timezone = 'Asia/Yekaterinburg'

app.conf.beat_schedule = {
    'parse_data': {
        'task': 'mainApp.tasks.parser_task',
        'schedule': crontab(minute=0, hour=settings.PARSER_HD_SCHEDULE)
    },
}
