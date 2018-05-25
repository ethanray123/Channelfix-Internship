from django.views import generic
from stream import models


class DetailView(generic.DetailView):
    model = models.Lobby
    template_name = 'stream/lobby/detail_view.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['streams'] = self.object.streams.order_by('-tag')
        context['comments'] = self.object.comments.order_by('-when')
        profile = models.Profile.objects.get(owner=self.request.user)
        if(not profile.is_viewed(self.object)):
            models.LobbyViews.objects.create(
                lobby=self.object,
                viewer=profile)
        return context
