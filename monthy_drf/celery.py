import os

from celery import Celery
from django.conf import settings

# DJANGO_SETTINGS_MODULE의 환경 변수를 설정해준다.
if not os.getenv('DJANGO_SETTINGS_MODULE'):
    raise RuntimeError('DJANGO_SETTINGS_MODULE 환경 변수가 설정되어 있지 않습니다.')
app = Celery('monthy_drf')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))