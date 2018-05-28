from django.views import generic
from stream.models import Subscription
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import Http404, JsonResponse


class SubscribeView(generic.View):
    """
    Used to subscribe or unsubscribe a user
    to an owner of a stream.
    """

    def post(self, request, *args, **kwargs):
        if not request.is_ajax():
            raise Http404

        info = {
            'subscriber': request.user,
            'publisher': get_object_or_404(
                User, pk=request.POST["streamer_id"])
        }
        has_subscribed = Subscription.objects.filter(**info).exists()
        if has_subscribed:
            Subscription.objects.get(**info).delete()
        else:
            Subscription.objects.create(**info)
        return JsonResponse(
            not has_subscribed, content_type="application/json", safe=False)
