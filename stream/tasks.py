from Project.celery import app
from .models import Profile
from django.utils import timezone
import datetime


@app.task
def check_online():

    offline_mark = timezone.now() - datetime.timedelta(minutes=1)

    Profile.objects.filter(
        last_seen__lt=offline_mark).update(online_status=False)
    Profile.objects.filter(
        last_seen__gte=offline_mark).update(online_status=True)
