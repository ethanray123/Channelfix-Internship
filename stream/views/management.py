from django.views import generic
from stream import models
from stream.forms import LobbyForm
from django.urls import reverse_lazy
from django.http import Http404, JsonResponse
from django.contrib.contenttypes.models import ContentType


class DetailView(generic.DetailView):
    model = models.Lobby
    template_name = 'stream/management/detail_view.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['streams'] = self.object.streams.order_by('-tag')
        context['comments'] = self.object.comments.order_by('when')
        ttype = ContentType.objects.get_for_model(models.Comment)
        reports = models.Report.objects.filter(content_type=ttype)
        results = []
        for report in reports:
            temp = {}
            if report.content_object.lobby.name == self.object.name:
                temp['id'] = report.content_id
                temp['comment_owner'] = report.content_object.owner
                temp['comment_text'] = report.content_object.text
                temp['commentremoved'] = report.content_object.removed
                temp['reason'] = report.get_reason
                temp['when'] = report.when
                results.append(temp)
        context['reports'] = results
        context['tags'] = models.STREAM_TAGS
        context['statuses'] = models.STATUS
        context['members'] = self.object.memberships.filter(status=2)
        context['requests'] = self.object.memberships.filter(status=0)
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
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise Http404
        return super(ModeratorView, self).dispatch(request, *args, **kwargs)

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
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.is_ajax():
            raise Http404
        return super(RemoveView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
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
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.is_ajax():
            raise Http404
        return super(TagsView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
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
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.is_ajax():
            raise Http404
        return super(StatusView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        member = models.LobbyMembership.objects.get(
            pk=request.POST['request_id'])
        member.status = request.POST['status']
        member.save()

        return JsonResponse(
            "data", content_type="application/json", safe=False)
