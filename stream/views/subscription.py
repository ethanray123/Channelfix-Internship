from django.views import generic
from stream import models
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import Http404, JsonResponse


class SubscribeView(generic.View):
    """
    Used to subscribe user to an owner of a stream via follow button.
    Passes a message if successful.
    """

    def get(self, request, *args, **kwargs):
        if not request.is_ajax():
            raise Http404

        subscriber = get_object_or_404(User, pk=request.user.id)
        subscribed_to = get_object_or_404(User, pk=request.GET["streamer_id"])
        has_subscribed = models.Subscription.objects.filter(
            subscriber=subscriber, publisher=subscribed_to).exists()
        if not has_subscribed:
            models.Subscription.objects.create(
                subscriber=subscriber,
                publisher=subscribed_to)
            message = "Successfully subscribed to " + subscribed_to.username
        else:
            subscription = models.Subscription.objects.get(
                subscriber=subscriber, publisher=subscribed_to)
            subscription.delete()
            message = "Successfully unsubscribed to " + subscribed_to.username
        data = {
            'message': message,
        }

        return JsonResponse(
            data, content_type="application/json", safe=False)
