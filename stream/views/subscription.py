from django.views import generic
from stream.models import Subscription
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.http import Http404, JsonResponse


class SubscribeView(generic.View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.is_ajax():
            raise Http404
        return super(SubscribeView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
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
