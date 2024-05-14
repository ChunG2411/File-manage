import os
from celery import Celery
from celery.schedules import crontab
from app_user.task import reset_limit

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "manage_file.settings")
app = Celery("django_celery")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute=1, hour=0),
        reset_limit.s(),
    )