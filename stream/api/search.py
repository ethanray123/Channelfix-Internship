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
            removed=False)[:5]
        user_results = []
        for obj in users:
            user = {}
            user['id'] = obj.pk,
            user['username'] = obj.owner.username,
            user['avatar'] = obj.avatar.url,
            user['nickname'] = obj.nickname,
            user['url'] = reverse(
                'stream:profile', args=[obj.pk])
            user_results.append(user)
        streams = models.Stream.objects.filter(
            title__icontains=text, removed=False)[:5]
        stream_results = []
        for obj in streams:
            stream = {}
            stream['id'] = obj.pk,
            stream['title'] = obj.title,
            stream['image'] = obj.image.url,
            stream['tag'] = obj.get_tag_display(),
            stream['url'] = reverse(
                'stream:lobby_detailview', args=[obj.lobby.pk])
            stream_results.append(stream)
        lobbies = models.Lobby.objects.filter(
            name__icontains=text,
            removed=False)[:5]
        lobby_results = []
        for obj in lobbies:
            lobby = {}
            lobby['id'] = obj.pk,
            lobby['name'] = obj.name,
            lobby['image'] = obj.image.url,
            lobby['type'] = obj.get_lobby_type_display()
            lobby['url'] = reverse(
                'stream:lobby_detailview', args=[obj.pk])
            lobby_results.append(lobby)
        data = {
            'streams': stream_results,
            'lobbies': lobby_results,
            'users': user_results}
        return JsonResponse(
            data, content_type="application/json", safe=False)
