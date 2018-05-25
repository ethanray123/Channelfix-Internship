from django.views import generic
from stream import models
from django.http import Http404
from django.shortcuts import get_object_or_404


class ViewersView(generic.View):

    def get(self, request, *args, **kwargs):
        if not request.is_ajax():
            raise Http404
        viewer = get_object_or_404(models.Profile, user=request.user)
        lobby = get_object_or_404(models.Lobby, pk=request.GET['lobby_id'])
        if(not viewer.is_viewed(lobby) and
           lobby.user.username != viewer.user.username):
            models.LobbyViews.objects.create(
                lobby=lobby,
                viewer=viewer)
