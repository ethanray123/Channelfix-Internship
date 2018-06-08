from django.views import generic
from stream.models import Profile
from stream import forms
from django.urls import reverse


class DetailView(generic.DetailView):
    model = Profile
    template_name = 'stream/profile/detail_view.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['is_subscribed'] = self.get_subscription_boolean()
        context['streams'] = self.get_streams()
        context['lobbies'] = self.get_lobbies()
        context['comments'] = self.get_comments()
        return context

    def get_streams(self):
        queryset = self.object.owner.streams.filter(
            removed=False).order_by('-tag')
        results = []
        for obj in queryset:
            temp = {}
            temp['lobby_id'] = obj.lobby.id
            temp['title'] = obj.title
            temp['owner'] = {
                'id': obj.owner.id
            }
            temp['tag'] = obj.get_tag_display()
            temp['image'] = obj.image
            temp['description'] = obj.description
            temp['when'] = obj.when
            results.append(temp)
        return results

    def get_lobbies(self):
        queryset = self.object.owner.lobbies.filter(
            removed=False).order_by('-lobby_type')
        results = []
        for obj in queryset:
            temp = {}
            temp['id'] = obj.id
            temp['name'] = obj.name
            temp['owner'] = {
                'id': obj.owner.id
            }
            temp['type'] = obj.get_lobby_type_display()
            temp['image'] = obj.image
            temp['description'] = obj.description
            temp['when'] = obj.when
            results.append(temp)
        return results

    def get_comments(self):
        queryset = self.object.owner.comments.filter(
            removed=False).order_by('-lobby')
        results = []
        for obj in queryset:
            temp = {}
            temp['id'] = obj.id
            temp['text'] = obj.text
            temp['owner'] = {
                'id': obj.owner.id
            }
            temp['lobby'] = obj.lobby.name
            temp['lobby_id'] = obj.lobby.id
            temp['when'] = obj.when
            results.append(temp)
        return results

    def get_subscription_boolean(self):
        return self.object.is_subscribed(self.request.user)


class UpdateView(generic.UpdateView):
    model = Profile
    form_class = forms.ProfileForm
    template_name = 'stream/profile/update_view.html'

    def get_success_url(self):
        return reverse('stream:profile', args=[self.object.pk])
