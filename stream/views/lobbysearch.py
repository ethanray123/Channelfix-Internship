from django.views import generic
from stream.models import Lobby
from django.http import Http404, JsonResponse


class LobbySearchView(generic.View):

    def get(self, request, *args, **kwargs):
        if not request.is_ajax():
            raise Http404

        querylength = Lobby.objects.filter(
            category=self.request.GET.get("category_pk", '')).count()
        print(querylength)
        return JsonResponse(
            querylength, content_type="application/json", safe=False)
