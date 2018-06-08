from django.views import generic
from stream.models import Profile
from django.http import Http404, JsonResponse

from django.utils import timezone


class OnlineView(generic.View):

    def post(self, request, *args, **kwargs):
        if not request.is_ajax():
            raise Http404

        now = timezone.now()
        profile = Profile.objects.get(pk=request.POST['pk'])
        print(request.POST['pk'])
        print(profile.owner.username)
        profile.last_seen = now
        profile.save()
        return JsonResponse(
            "data",
            content_type="application/json",
            safe=False
        )
