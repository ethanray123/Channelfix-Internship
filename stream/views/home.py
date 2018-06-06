from django.views import generic
from stream import models


class HomeView(generic.TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['lobbies'] = models.Lobby.objects.all()
        context['notifications'] = self.get_notifications()
        return context

    def get_lobbies(self):
        queryset = models.Lobby.objects.all()
        results = []
        for obj in queryset:
            temp = {}
            temp['id'] = obj.id
            temp['image'] = obj.image
            temp['name'] = obj.name
            temp['owner'] = {
                'id': obj.owner.id,
                'username': obj.owner.username,
                'is_subscribed': obj.owner.profile.is_subscribed(
                    self.request.user),
                'profile_id': obj.owner.profile.id
            }
            temp['description'] = obj.description
            results.append(temp)
        return results

    def get_notifications(self):
        queryset = self.request.user.notifications.all().order_by("-when")
        results = []
        for obj in queryset:
            temp = {}
            temp['target_type'] = obj.target_type
            temp['target_id'] = obj.target_id
            temp['target_object'] = obj.target_object
            temp['details'] = obj.get_notification
            temp['owner'] = {
                'id': obj.owner.id,
                'username': obj.owner.username,
                'is_subscribed': obj.owner.profile.is_subscribed(
                    self.request.user),
                'profile_id': obj.owner.profile.id
            }
            temp['when'] = obj.when
            results.append(temp)
        return results
