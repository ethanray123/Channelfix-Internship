from django.views import generic
from stream import models
from django.db.models import Count


class HomeView(generic.TemplateView):
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['lobbies'] = self.get_lobbies()
        context['online_users'] = self.get_users()
        context['stats'] = self.get_stats()
        if(self.request.user.is_authenticated):
            context['notifications'] = self.get_notifications()
            context['fav_lobbies'] = self.get_favorites()
        context['categories'] = models.Category.objects.all()
        return context

    def get_favorites(self):
        queryset = self.request.user.favorites.all().order_by(
            "lobby__name")[:10]
        results = []
        for obj in queryset:
            temp = {}
            temp['id'] = obj.lobby.id
            temp['image'] = obj.lobby.image
            temp['name'] = obj.lobby.name
            temp['owner'] = {
                'id': obj.lobby.owner.id,
                'username': obj.lobby.owner.username,
                'avatar': obj.lobby.owner.profile.avatar,
                'profile_id': obj.lobby.owner.profile.id
            }
            temp['description'] = obj.lobby.description
            temp['streams'] = obj.lobby.streams.all().count()
            results.append(temp)
        return results

    def get_lobbies(self):
        if self.request.GET.get("category_pk", '') != "":
            queryset = models.Lobby.objects.all().filter(
                category=int(
                    self.request.GET.get(
                        "category_pk", ''))).order_by("-when")[:10]
        else:
            queryset = models.Lobby.objects.all().order_by("-when")[:10]
        results = []
        for obj in queryset:
            temp = {}
            temp['id'] = obj.id
            temp['image'] = obj.image
            temp['name'] = obj.name
            temp['owner'] = {
                'id': obj.owner.id,
                'username': obj.owner.username,
                'avatar': obj.owner.profile.avatar,
                'profile_id': obj.owner.profile.id
            }
            temp['description'] = obj.description
            temp['streams'] = obj.streams.filter(removed=False).count()
            temp['views'] = obj.views.all().count()
            temp['category'] = obj.category
            temp['when'] = obj.when
            results.append(temp)
        return results

    def get_users(self):
        queryset = models.User.objects.all()[:10]
        results = []
        for obj in queryset:
            temp = {}
            temp['username'] = obj.username
            temp['profile_id'] = obj.profile.id
            temp['avatar'] = str(obj.profile.avatar.url)
            results.append(temp)
        return results

    def get_notifications(self):
        queryset = self.request.user.notifications.all().order_by("-when")[:5]
        results = []
        for obj in queryset:
            temp = {}
            temp['target_type'] = str(obj.target_type)
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

    def get_stats(self):
        temp = {}
        user = models.User.objects.all().annotate(
            sub_count=Count('publishers')).order_by('-sub_count').first()
        temp['most_followed'] = user
        user = models.User.objects.all().annotate(
            stream_count=Count('streams')).order_by('-stream_count').first()
        temp['most_streams'] = user
        user = models.User.objects.all().annotate(
            lobby_count=Count('lobbies')).order_by('-lobby_count').first()
        temp['most_lobbies'] = user
        game = models.Category.objects.all().annotate(
            lobby_count=Count('lobby')).order_by('-lobby_count').first()
        temp['popular_game'] = game.name
        return temp
