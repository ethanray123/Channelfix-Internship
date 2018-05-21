from django.views import generic
from stream import models


class HomeView(generic.TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['lobbies'] = models.Lobby.objects.all()
        return context
