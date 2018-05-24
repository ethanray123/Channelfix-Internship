from django.views import generic
from stream import models
from django.http import Http404, JsonResponse
from django.contrib.contenttypes.models import ContentType


class DetailView(generic.DetailView):
    model = models.Lobby
    template_name = 'stream/lobby/detail_view.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['streams'] = self.object.streams.filter(
            removed=False).order_by('-tag')
        context['comments'] = self.object.comments.filter(
            removed=False).order_by('-when')
        return context


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
        comments = lobby.comments.values(
            'pk', 'text', 'owner__username', 'when',
            'owner__profile__avatar').filter(removed=False).order_by('-when')
        data = {'comments': list(comments)}
        return JsonResponse(
            data,
            content_type="application/json",
            safe=False)
