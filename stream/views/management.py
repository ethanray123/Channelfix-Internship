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
        if self.object.has_main():
            context['main'] = self.object.get_main()
        return context


class LobbyFormView(generic.UpdateView):
    model = models.Lobby
    form_class = LobbyForm
    template_name = "stream/management/edit.html"

    def get_success_url(self):
        return reverse_lazy('stream:home')


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
            user = models.Profile.objects.get(pk=request.POST['pk'])
            lobby = models.Lobby.objects.get(pk=kwargs.get('pk'))
            member = models.LobbyMembership.objects.get(
                member=user, lobby=lobby)
            if request.POST['value'] == "true":
                value = True
            member.removed = value
            member.save()
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
