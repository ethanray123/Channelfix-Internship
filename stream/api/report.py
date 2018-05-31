from django.views import generic
from stream.models import Report, Stream, Comment
from django.http import Http404, JsonResponse


class ReportAPI(generic.View):
    model = Report

    def get(self, request, *args, **kwargs):
        if not request.is_ajax():
            raise Http404
        # Create queryset.
        queryset = self.model.objects.exclude(removed=True).order_by('-when')

        # Get offset.
        queryset = queryset[int(request.GET['start']):int(request.GET['end'])]

        # Generate response.
        response = []
        for obj in queryset:
            data = {}
            data['id'] = obj.pk
            data['reporter'] = {
                'id': obj.reporter.pk,
                'username': obj.reporter.username
            }
            if isinstance(obj.content_object, Stream):
                data['stream'] = {
                    'id': obj.content_object.pk,
                    'owner': {
                        'id': obj.content_object.lobby.owner.pk,
                        'username': obj.content_object.lobby.owner.username
                    },
                    'lobby': {
                        'id': obj.content_object.lobby.pk,
                        'name': obj.content_object.lobby.name,
                        'owner': {
                            'id': obj.content_object.lobby.owner.pk,
                            'username': obj.content_object.lobby.owner.username
                        }
                    },
                    'image': obj.content_object.image.url,
                    'title': obj.content_object.title,
                    'URL': obj.content_object.URL,
                    'description': obj.content_object.description,
                    'tag': obj.content_object.tag,
                    'when': obj.content_object.when.strftime("%b %d, %Y at %I:%M:%S %p"),
                    'removed': obj.content_object.removed
                }
            elif isinstance(obj.content_object, Comment):
                data['comment'] = {
                    'id': obj.content_object.pk,
                    'owner': {
                        'id': obj.content_object.lobby.owner.pk,
                        'username': obj.content_object.lobby.owner.username
                    },
                    'lobby': {
                        'id': obj.content_object.lobby.pk,
                        'name': obj.content_object.lobby.name,
                        'owner': {
                            'id': obj.content_object.lobby.owner.pk,
                            'username': obj.content_object.lobby.owner.username
                        }
                    },
                    'when': obj.content_object.when.strftime("%b %d, %Y at %I:%M:%S %p"),
                    'removed': obj.content_object.removed
                }
            data['when'] = obj.when.strftime("%b %d, %Y at %I:%M:%S %p")
            data['removed'] = obj.removed
            # List all fields here
            response.append(data)

        return JsonResponse(
            response, content_type="application/json", safe=False)
