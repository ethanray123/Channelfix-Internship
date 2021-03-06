from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from stream import models
from django.http import Http404, JsonResponse
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from stream import forms


class DetailView(generic.DetailView):
    model = models.Lobby
    template_name = 'stream/lobby/detail_view.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(
                reverse('login'))
        return super(DetailView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        profile = models.Profile.objects.get(owner=self.request.user)
        if(not profile.is_viewed(self.object)):
            models.LobbyViews.objects.create(
                lobby=self.object,
                viewer=profile)
        context['streams'] = self.get_streams()
        context['is_moderator'] = self.object.moderators.filter(
            owner=self.request.user).exists()
        context['comments'] = self.object.comments.filter(
            removed=False).order_by('-when')
        context['is_member'] = self.object.is_member(profile)
        context['is_requesting'] = profile.memberships.filter(
            lobby=self.object, status=models.LobbyMembership.PENDING,
            removed=False).exists()
        context['has_stream'] = self.object.streams.filter(
            owner=self.request.user, removed=False).exists()
        context['is_favorite'] = self.object.favorites.filter(
            owner=self.request.user).exists()
        context['is_subscribed'] = self.object.owner.profile.is_subscribed(
            self.request.user)
        try:
            context['my_stream'] = self.object.streams.get(
                owner=self.request.user, removed=False)
        except models.Stream.DoesNotExist:
            pass
        context['statistics'] = self.getStats()
        return context

    def get_streams(self):
        queryset = self.object.streams.filter(
            removed=False).order_by('-tag')
        results = []
        for obj in queryset:
            temp = {}
            temp['id'] = obj.id
            temp['title'] = obj.title
            temp['owner'] = {
                'id': obj.owner.id,
                'username': obj.owner.username,
                'is_subscribed': obj.owner.profile.is_subscribed(
                    self.request.user),
                'profile_id': obj.owner.profile.id,
                'avatar': obj.owner.profile.avatar.url
            }
            temp['session_id'] = obj.session_id
            temp['pub_token'] = obj.pub_token
            temp['sub_token'] = obj.sub_token
            temp['description'] = obj.description
            temp['tag'] = obj.get_tag_display()
            temp['image'] = obj.image
            results.append(temp)
        return results

    def getStats(self):
        stats = {
            'views': self.object.views.count(),
            'faves': self.object.favorites.count(),
            'members': self.object.memberships.filter(
                status=models.LobbyMembership.ACCEPTED).count(),
            'comments': self.object.comments.filter(removed=False).count(),
            'streams': self.object.streams.filter(removed=False).count(),
            'sponsors': self.object.streams.filter(
                tag=1, removed=False).count(),
            'players': self.object.streams.filter(
                tag=2, removed=False).count()
        }
        return stats


class CommentView(generic.View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.is_ajax():
            raise Http404
        return super(CommentView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        lobby = models.Lobby.objects.get(pk=kwargs.get('pk'))
        if request.POST['type'] == "create":
            comment = models.Comment.objects.create(
                lobby=lobby,
                text=request.POST['txtComment'],
                owner=request.user)
        elif request.POST['type'] == "remove":
            comment = models.Comment.objects.get(
                pk=request.POST['pk'], owner=request.user)
            comment.removed = True
            comment.save()
        elif request.POST['type'] == "report":
            comment = models.Comment.objects.get(pk=request.POST['pk'])
            if not comment.is_reported(self.request.user):
                content_type = ContentType.objects.get_for_model(
                    models.Comment)
                models.Report.objects.create(
                    reporter=self.request.user, content_type=content_type,
                    content_id=comment.pk, reason=request.POST['reason'])
        data = {'pk': comment.pk, 'text': comment.text,
                'owner': comment.owner.username, 'when': comment.when}
        return JsonResponse(data, content_type="application/json", safe=False)

    def get(self, request, *args, **kwargs):
        lobby = models.Lobby.objects.get(pk=kwargs.get('pk'))
        comments = lobby.comments.filter(removed=False).order_by('-when')
        comment_list = []
        for comment in comments:
            temp = {}
            temp['pk'] = comment.pk
            temp['text'] = comment.text
            temp['isreported'] = comment.is_reported(request.user)
            temp['owner__profile__avatar'] = str(comment.owner.profile.avatar)
            temp['owner__username'] = comment.owner.username
            temp['when'] = comment.when.strftime("%b %d, %Y at %I:%M:%S %p")
            comment_list.append(temp)
        data = {'comments': comment_list}
        return JsonResponse(
            data,
            content_type="application/json",
            safe=False)


class RequestMembershipView(generic.View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.is_ajax():
            raise Http404
        return super(RequestMembershipView, self).dispatch(
            request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        lobby = models.Lobby.objects.get(pk=kwargs.get('pk'))

        if request.user.profile.memberships.filter(
            lobby=lobby, status=models.LobbyMembership.PENDING,
                removed=False).exists():
            return HttpResponse("Existing request!")

        models.LobbyMembership.objects.create(
            member=request.user.profile, lobby=lobby,
            status=models.LobbyMembership.PENDING)
        return HttpResponse("Success!")


class FavoriteView(generic.View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise Http404
        return super(FavoriteView, self).dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        lobby = models.Lobby.objects.get(pk=kwargs.get('pk'))
        if(request.POST['type'] == 'favorite'):
            models.Favorite.objects.create(owner=request.user, lobby=lobby)
        elif(request.POST['type'] == 'unfavorite'):
            models.Favorite.objects.filter(
                owner=request.user, lobby=lobby).delete()
        return HttpResponse("success")


class CreateView(generic.CreateView):
    model = models.Lobby
    form_class = forms.LobbyForm
    template_name = 'stream/lobby/create_view.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise Http404
        return super(CreateView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        lobby = form.save(commit=False)
        lobby.owner = self.request.user
        lobby.save()
        models.LobbyMembership.objects.create(
            member=self.request.user.profile, lobby=lobby,
            status=models.LobbyMembership.ACCEPTED)
        return HttpResponseRedirect(
            reverse('stream:lobby_detailview', args=[lobby.id]))
