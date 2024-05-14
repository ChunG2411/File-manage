from django.core.mail import send_mail
from django.conf import settings
from .models import LimitAction

from celery import shared_task


@shared_task()
def send_email_task(email, code_char):
    send_mail(
        "Register Code",
        "Please enter this code to register page: {}".format(code_char),
        settings.EMAIL_HOST_USER,
        ['{}@gmail.com'.format(email)]
    )


@shared_task()
def reset_limit():
    objects = LimitAction.objects.all()
    for i in objects:
        i.upload = 0
        i.download = 0
        i.save()
        print('Reseted {i.user}')
