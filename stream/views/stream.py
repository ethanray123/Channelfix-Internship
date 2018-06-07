from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.views import generic
from django.urls import reverse
from stream import models
from stream import forms
from opentok import OpenTok, Roles
import base64

api_key = "46119842"
api_secret = "a061d4a5aa1e22cf68b449dcbdd05ce3e403b0f4"

opentok = OpenTok(api_key, api_secret)


class CreateView(generic.CreateView):
    model = models.Stream
    form_class = forms.StreamForm
    template_name = 'stream/stream/create_view.html'

    def dispatch(self, request, *args, **kwargs):
        lobby = models.Lobby.objects.get(pk=self.kwargs.get('pk'))
        if(lobby.is_private()):
            if(not lobby.is_member(self.request.user.profile)):
                raise Http404
        if(lobby.has_stream(self.request.user)):
            raise Http404
        return super(CreateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        context['lobby'] = models.Lobby.objects.get(pk=self.kwargs.get('pk'))
        return context

    def form_valid(self, form):
        lobby = models.Lobby.objects.get(pk=self.kwargs.get('pk'))
        session = opentok.create_session()
        stream = form.save(commit=False)
        stream.owner = self.request.user
        stream.lobby = lobby
        stream.session_id = session.session_id
        stream.pub_token = opentok.generate_token(
            session.session_id,
            role=Roles.publisher
        )
        stream.sub_token = opentok.generate_token(
            session.session_id,
            Roles.subscriber)
        self.object = stream.save()
        return HttpResponseRedirect(
            reverse('stream:publisher_view', args=[lobby.id, stream.id]))


class UpdateView(generic.UpdateView):
    model = models.Stream
    form_class = forms.StreamForm
    template_name = 'stream/stream/update_view.html'

    def get_success_url(self):
        return reverse(
            'stream:publisher_view',
            args=[self.object.lobby.pk, self.object.id])


class DeleteView(generic.DeleteView):
    model = models.Stream

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.removed = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('stream:lobby_detailview', args=[self.object.lobby.pk])


class PublisherView(generic.DetailView):
    model = models.Stream
    template_name = 'stream/stream/publisher.html'

    def dispatch(self, request, *args, **kwargs):
        if(not self.get_object().owner == request.user or
                self.get_object().removed):
            raise Http404
        return super(PublisherView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PublisherView, self).get_context_data(**kwargs)
        return context


class GetImage(generic.View):

    def post(self, request, *args, **kwargs):
        image_data = base64.b64decode(request.POST['image'])
        filename = 'stream/static/images/stream_image' \
            + request.POST['pk'] + '.png'
        with open("media/" + filename, 'wb') as f:
            f.write(image_data)
        f.close()
        stream = models.Stream.objects.get(pk=request.POST['pk'])
        stream.image = filename
        stream.save()
        return HttpResponse('success')


class RemoveView(generic.View):

    def post(self, request, *args, **kwargs):
        stream = models.Stream.objects.get(pk=kwargs.get('pk'))
        if (not stream.removed):
            stream.removed = True

        stream.save()
        return HttpResponseRedirect(
            reverse('stream:lobby_detailview', args=[stream.lobby.pk]))
