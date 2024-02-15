from time import sleep
from celery import shared_task
from django.core.cache import cache
from .models import Truck

from django.conf import settings
# from logistics.celery import app


# @app.task
@shared_task
def notify_customers(message):
    print("*** Sending 1000 messages....")
    print("***", message)
    sleep(3)
    print("*** Emails were successfully sent!")

