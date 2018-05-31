from django.views import generic
from stream.models import Profile
from django.http import Http404, JsonResponse


class ProfileAPI(generic.View):
    model = Profile

    def get(self, request, *args, **kwargs):
        if not request.is_ajax():
            raise Http404
        # Create queryset.
        queryset = self.model.objects.exclude(removed=True)
        # Get offset.
        queryset = queryset[int(request.GET['start']):int(request.GET['end'])]

        # Generate response.
        response = []
        for obj in queryset:
            data = {}
            data['id'] = obj.pk
            data['owner'] = {
                'id': obj.owner.pk,
                'username': obj.owner.username
            }
            data['nickname'] = obj.nickname
            data['avatar'] = obj.avatar.url
            data['when'] = obj.when.strftime("%b %d, %Y at %I:%M:%S %p")
            data['removed'] = obj.removed
            # List all fields here
            response.append(data)

        return JsonResponse(
            response, content_type="application/json", safe=False)
