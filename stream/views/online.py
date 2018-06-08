from django.views import generic
from stream.models import Profile
from django.http import Http404, JsonResponse
from django.utils import timezone


class OnlineView(generic.View):

    def post(self, request, *args, **kwargs):
        if not request.is_ajax():
            raise Http404

        if not request.user.is_authenticated:
            raise Http404

        profile = Profile.objects.get(pk=request.user.profile.id)
        profile.last_seen = timezone.now()
        profile.save()
        return JsonResponse(
            "data",
            content_type="application/json",
            safe=False
        )
