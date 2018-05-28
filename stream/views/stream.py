from django.http import HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from stream import models
from stream import forms


class CreateView(generic.CreateView):
    model = models.Stream
    form_class = forms.StreamForm
    template_name = 'stream/stream/create_view.html'

    def form_valid(self, form):
        lobby = models.Lobby.objects.get(pk=self.kwargs.get('pk'))
        if not lobby.has_stream(self.request.user):
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


class DeleteView(generic.DeleteView):
    model = models.Stream

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.removed = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('stream:lobby_detailview', args=[self.object.lobby.pk])
