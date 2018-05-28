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
        return context


class LobbyFormView(generic.UpdateView):
    model = models.Lobby
    form_class = LobbyForm
    template_name = "stream/management/edit.html"

    def get_success_url(self):
        return reverse_lazy('stream:home')


class RemoveView(generic.View):
    def get(self, request, *args, **kwargs):
        if not request.is_ajax():
            raise Http404
        if request.GET['model'] == "stream":
            stream = models.Stream.objects.get(pk=request.GET['pk'])
            value = False
            if request.GET['value'] == "true":
                value = True
            stream.removed = value
            stream.save()
        elif request.GET["model"] == "member":
            print("dsds")
            user = models.Profile.objects.get(pk=request.GET['pk'])
            lobby = models.Lobby.objects.get(pk=kwargs.get('pk'))
            member = models.LobbyMembership.objects.get(
                member=user, lobby=lobby)
            value = False
            if request.GET['value'] == "true":
                value = True
            member.removed = value
            member.save()
        elif request.GET['model'] == "comment":
            comment = models.Comment.objects.get(pk=request.GET['pk'])
            value = False
            if request.GET['value'] == "true":
                value = True
            comment.removed = value
            comment.save()
        return JsonResponse(
            "data", content_type="application/json", safe=False)


class TagsView(generic.View):
    def get(self, request, *args, **kwargs):
        if not request.is_ajax():
            raise Http404
        lobby = models.Lobby.objects.get(pk=kwargs.get('pk'))
        stream = models.Stream.objects.get(
            pk=request.GET['stream_id'], lobby=lobby)
        stream.tag = request.GET['tag']
        stream.save()
        return JsonResponse(
            "data", content_type="application/json", safe=False)
