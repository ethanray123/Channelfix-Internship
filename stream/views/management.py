from django.views import generic
from stream import models
from stream.forms import LobbyForm
from django.urls import reverse_lazy


class DetailView(generic.DetailView):
    model = models.Lobby
    template_name = 'stream/management/detail_view.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['streams'] = self.object.streams.order_by('-tag')
        context['comments'] = self.object.comments.order_by('when')
        return context


class LobbyFormView(generic.UpdateView):
    model = models.Lobby
    form_class = LobbyForm
    template_name = "stream/management/edit.html"

    def get_success_url(self):
        return reverse_lazy('stream:home')
