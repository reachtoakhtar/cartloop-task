import os
import django
from celery import Celery
from celery.schedules import crontab
from decouple import config
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api.settings')
django.setup()

app = Celery('api')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.task_default_queue = settings.CELERY_TASK_DEFAULT_QUEUE

app.conf.beat_schedule = {
    # 'send-mail': {
    #     'task': 'api.chat.tasks.send_mail',
    #     'schedule': crontab(minute="*/20"),
    # },
}


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
