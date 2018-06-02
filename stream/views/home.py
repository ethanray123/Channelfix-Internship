from django.views import generic
from stream import models


class HomeView(generic.TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['lobbies'] = models.Lobby.objects.all()
        if(self.request.user.is_authenticated):
            context['notifications'] = self.get_notifications()
        return context

    def get_notifications(self):
        queryset = models.Notification.objects.filter(
            owner=self.request.user).order_by('-when')[:5]
        results = []
        for obj in queryset:
            temp = {}
            temp['description'] = obj.get_notification
            temp['when'] = obj.when
            results.append(temp)
        return results
