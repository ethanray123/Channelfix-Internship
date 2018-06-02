from django.views import generic
from stream.models import Subscription
from django.http import Http404, JsonResponse


class SubscriptionAPI(generic.View):
    model = Subscription

    def get(self, request, *args, **kwargs):
        if not request.is_ajax():
            raise Http404
        # Create queryset.
        queryset = self.model.objects.filter(
            subscriber__pk=request.GET['subsciber__pk'])

        # Get offset.
        queryset = queryset[int(request.GET['start']):int(request.GET['end'])]

        # Generate response.
        response = []
        for obj in queryset:
            data = {}
            data['id'] = obj.pk
            data['subscriber'] = {
                'id': obj.subscriber.pk,
                'username': obj.subscriber.username
            }
            data['publisher'] = {
                'id': obj.publisher.pk,
                'username': obj.publisher.username
            }
            # List all fields here
            response.append(data)

        return JsonResponse(
            response, content_type="application/json", safe=False)
