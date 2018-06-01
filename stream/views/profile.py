from django.views import generic
from stream.models import Profile


class DetailView(generic.DetailView):
    model = Profile
    template_name = 'stream/profile/detail_view.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['is_subscribed'] = self.get_subscription_boolean()
        context['streams'] = self.object.owner.streams.order_by('-tag')
    #     context['lobbies'] = self.object.lobbies.order_by('when')
    #     context['reports'] = self.object.comments.filter(
    # report__isnull=False)
    #     if self.object.has_main():
    #         context['main'] = self.object.get_main()
        return context

    def get_subscription_boolean(self):
        return self.object.is_subscribed(self.request.user)
