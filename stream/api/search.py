from django.views import generic
from django.http import Http404, JsonResponse
from stream import models
from django.urls import reverse


class SearchAPI(generic.View):

    def get(self, request, *args, **kwargs):
        if not request.is_ajax():
            raise Http404
        text = request.GET['text']
        users = models.Profile.objects.filter(
            owner__username__icontains=text,
            removed=False)[:3]
        user_results = []
        for obj in users:
            user = {}
            user['title'] = obj.owner.username,
            if obj.avatar:
                user['image'] = obj.avatar.url,
            else:
                user['image'] = "/media/stream/static/images/default_avatar.png"
            user['description'] = obj.nickname,
            user['url'] = reverse(
                'stream:profile', args=[obj.pk])
            user_results.append(user)
        streams = models.Stream.objects.filter(
            title__icontains=text, removed=False)[:3]
        stream_results = []
        for obj in streams:
            stream = {}
            stream['title'] = obj.title,
            if obj.image:
                stream['image'] = obj.image.url,
            else:
                stream['image'] = "/media/stream/static/images/default_thumbnail.jpg"
            stream['description'] = obj.get_tag_display(),
            stream['url'] = reverse(
                'stream:lobby_detailview', args=[obj.lobby.pk])
            stream_results.append(stream)
        lobbies = models.Lobby.objects.filter(
            name__icontains=text,
            removed=False)[:3]
        lobby_results = []
        for obj in lobbies:
            lobby = {}
            lobby['title'] = obj.name,
            if obj.image:
                lobby['image'] = obj.image.url,
            else:
                lobby['image'] = "/media/stream/static/images/default_thumbnail.jpg",
            lobby['description'] = obj.get_lobby_type_display()
            lobby['url'] = reverse(
                'stream:lobby_detailview', args=[obj.pk])
            lobby_results.append(lobby)

        data = {
            'results': {
                'streams': {'name': 'STREAM', 'results': stream_results},
                'lobbies': {'name': 'LOBBY', 'results': lobby_results},
                'users': {'name': 'USER', 'results': user_results}
            }
        }
        return JsonResponse(
            data, content_type="application/json", safe=False)
