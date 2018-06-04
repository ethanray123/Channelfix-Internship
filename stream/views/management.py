from django.views import generic
from stream import models
from stream.forms import LobbyForm
from django.urls import reverse_lazy
from django.http import Http404, JsonResponse


class DetailView(generic.DetailView):
    model = models.Lobby
    template_name = 'stream/management/detail_view.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['streams'] = self.object.streams.order_by('-tag')
        context['comments'] = self.object.comments.order_by('when')
        context['reports'] = self.object.comments.filter(report__isnull=False)
        context['tags'] = models.STREAM_TAGS
        context['statuses'] = models.STATUS
        context['members'] = self.object.memberships.filter(status=2)
        context['requests'] = self.object.memberships.filter(status=0)
        # context['moderators'] = self.object.moderators.order_by('owner')
        context['is_moderator'] = self.object.is_moderator(self.request.user)
        if self.object.has_main():
            context['main'] = self.object.get_main()
        return context


class LobbyFormView(generic.UpdateView):
    model = models.Lobby
    form_class = LobbyForm
    template_name = "stream/management/edit.html"

    def get_success_url(self):
        return reverse_lazy('stream:home')


class ModeratorView(generic.View):
    def post(self, request, *args, **kwargs):
        cond = models.Moderator.objects.filter(
            owner__username=request.POST['user']).exists()
        if cond is True:
            moderator = models.Moderator.objects.get(
                owner__username=request.POST['user'])
            if request.POST['value'] == "true":
                value = False
            else:
                value = True
            moderator.removed = value
            moderator.save()
        else:
            lobby = models.Lobby.objects.get(pk=kwargs.get('pk'))
            owner = models.User.objects.get(
                username=request.POST['user'])
            new = models.Moderator.objects.create(owner=owner, lobby=lobby)
            new.save()
        return JsonResponse(
            "data", content_type="application/json", safe=False)


class RemoveView(generic.View):
    def post(self, request, *args, **kwargs):
        if not request.is_ajax():
            raise Http404
        value = False
        if request.POST['model'] == "stream":
            stream = models.Stream.objects.get(pk=request.POST['pk'])
            if request.POST['value'] == "true":
                value = True
            stream.removed = value
            stream.save()
        elif request.POST["model"] == "member":
            member = models.LobbyMembership.objects.get(pk=request.POST['pk'])
            lobby = models.Lobby.objects.get(pk=kwargs.get('pk'))
            stream = models.Stream.objects.get(
                owner__username=member, lobby=lobby)
            if request.POST['value'] == "true":
                value = True
            member.removed = value
            stream.removed = value
            member.save()
            stream.save()
        elif request.POST['model'] == "comment":
            comment = models.Comment.objects.get(pk=request.POST['pk'])
            if request.POST['value'] == "true":
                value = True
            comment.removed = value
            comment.save()
        return JsonResponse(
            "data", content_type="application/json", safe=False)


class TagsView(generic.View):
    def post(self, request, *args, **kwargs):
        if not request.is_ajax():
            raise Http404
        data = ""
        lobby = models.Lobby.objects.get(pk=kwargs.get('pk'))
        if lobby.has_main() and request.POST['tag'] == '3':
            main_stream = lobby.get_main()
            main_stream.tag = request.POST['changed_tag']
            main_stream.save()
        stream = models.Stream.objects.get(
            pk=request.POST['stream_id'], lobby=lobby)
        stream.tag = request.POST['tag']
        stream.save()
        return JsonResponse(
            data, content_type="application/json", safe=False)

    def get(self, request, *args, **kwargs):
        if not request.is_ajax():
            raise Http404
        lobby = models.Lobby.objects.get(pk=kwargs.get('pk'))
        streams = lobby.streams.order_by('-tag')
        stream_list = []
        for obj in streams:
            stream = {}
            stream['id'] = obj.id
            stream['tag'] = obj.tag
            stream['tag_display'] = obj.get_tag_display()
            stream_list.append(stream)
        temp = {}
        if lobby.has_main():
            main = lobby.get_main()
            temp['id'] = main.pk
        data = {
            'streams': list(stream_list),
            'main': temp
        }
        return JsonResponse(
            data,
            content_type="application/json",
            safe=False)


class StatusView(generic.View):
    def post(self, request, *args, **kwargs):
        if not request.is_ajax():
            raise Http404
        member = models.LobbyMembership.objects.get(
            pk=request.POST['request_id'])
        member.status = request.POST['status']
        member.save()

        return JsonResponse(
            "data", content_type="application/json", safe=False)
