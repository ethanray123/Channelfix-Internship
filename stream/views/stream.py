from django.http import HttpResponseRedirect, Http404
from django.views import generic
from django.urls import reverse
from stream import models
from stream import forms


class CreateView(generic.CreateView):
    model = models.Stream
    form_class = forms.StreamForm
    template_name = 'stream/stream/create_view.html'

    def dispatch(self, request, *args, **kwargs):
        lobby = models.Lobby.objects.get(pk=self.kwargs.get('pk'))
        if(lobby.is_private()):
            if(not lobby.is_member(self.request.user.profile)):
                raise Http404
        if(lobby.has_stream(self.request.user)):
            raise Http404
        return super(CreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        context['lobby'] = models.Lobby.objects.get(pk=self.kwargs.get('pk'))
        return context

    def form_valid(self, form):
        lobby = models.Lobby.objects.get(pk=self.kwargs.get('pk'))
        stream = form.save(commit=False)
        stream.owner = self.request.user
        stream.lobby = lobby
        self.object = stream.save()
        return HttpResponseRedirect(
            reverse('stream:lobby_detailview', args=[lobby.pk]))


class UpdateView(generic.UpdateView):
    model = models.Stream
    form_class = forms.StreamForm
    template_name = 'stream/stream/update_view.html'

    def get_success_url(self):
        return reverse('stream:lobby_detailview', args=[self.object.lobby.pk])


class RemoveView(generic.View):

    def post(self, request, *args, **kwargs):
        stream = models.Stream.objects.get(pk=kwargs.get('pk'))
        if (not stream.removed):
            stream.removed = True
        
        stream.save()
        return HttpResponseRedirect(
            reverse('stream:lobby_detailview', args=[stream.lobby.pk]))
