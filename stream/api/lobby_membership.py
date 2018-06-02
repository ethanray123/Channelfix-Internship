from django.views import generic
from stream.models import LobbyMembership
from django.http import Http404, JsonResponse


class LobbyMembershipAPI(generic.View):
    model = LobbyMembership

    def get(self, request, *args, **kwargs):
        if not request.is_ajax():
            raise Http404
        # Create queryset.
        queryset = self.model.objects.exclude(removed=True)
        queryset = queryset.filter(
            lobby__pk=request.GET['lobby__pk']).order_by('-when')

        # Get offset.
        queryset = queryset[int(request.GET['start']):int(request.GET['end'])]

        # Generate response.
        response = []
        for obj in queryset:
            data = {}
            data['id'] = obj.pk
            data['member'] = {
                'id': obj.member.owner.pk,
                'username': obj.member.owner.username
            }
            data['lobby'] = {
                'id': obj.lobby.pk,
                'name': obj.lobby.name,
                'owner': {
                    'id': obj.lobby.owner.pk,
                    'username': obj.lobby.owner.username
                }
            }
            data['when'] = obj.when.strftime("%b %d, %Y at %I:%M:%S %p")
            data['removed'] = obj.removed
            # List all fields here
            response.append(data)

        return JsonResponse(
            response, content_type="application/json", safe=False)
