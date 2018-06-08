from Project.celery import app
from .models import Profile
from django.utils import timezone
import datetime


@app.task
def check_online():

    profiles = Profile.objects.all()

    for profile in profiles:
        offline_mark = timezone.now() - datetime.timedelta(seconds=1)
        if(profile.last_seen < offline_mark):
            profile.online_status = False
        else:
            profile.online_status = True
        profile.save()
