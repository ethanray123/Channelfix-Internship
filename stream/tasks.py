from Project.celery import app
from .models import Profile
from django.utils import timezone
import datetime


@app.task
def check_online():

    exclude_mark = timezone.now() - datetime.timedelta(minutes=10)
    profiles = Profile.objects.filter(last_seen__gt=exclude_mark)
    offline_mark = timezone.now() - datetime.timedelta(minutes=1)

    for profile in profiles:
        if(profile.last_seen < offline_mark):
            profile.online_status = False
        else:
            profile.online_status = True
        profile.save()
