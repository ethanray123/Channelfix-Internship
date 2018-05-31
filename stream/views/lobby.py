from django.views import generic
from stream import models
from django.http import Http404, JsonResponse
from django.contrib.contenttypes.models import ContentType


class DetailView(generic.DetailView):
    model = models.Lobby
    template_name = 'stream/lobby/detail_view.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        profile = models.Profile.objects.get(owner=self.request.user)
        if(not profile.is_viewed(self.object)):
            models.LobbyViews.objects.create(
                lobby=self.object,
                viewer=profile)
        context['streams'] = self.get_streams()
        context['comments'] = self.object.comments.filter(
            removed=False).order_by('-when')
        context['is_member'] = self.object.is_member(profile)
        if(not self.object.owner == self.request.user):
            context['has_stream'] = self.object.streams.filter(
                owner=self.request.user, removed=False).exists()
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
                    self.request.user)
            }
            temp['tag'] = obj.get_tag_display()
            temp['image'] = obj.image
            results.append(temp)
        return results


class CommentView(generic.View):

    def post(self, request, *args, **kwargs):
        if not request.is_ajax():
            raise Http404
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
        if not request.is_ajax():
            raise Http404
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
            temp['when'] = comment.when
            comment_list.append(temp)
        data = {'comments': comment_list}
        return JsonResponse(
            data,
            content_type="application/json",
            safe=False)
