from django.views import generic
from stream.models import Lobby, User
from django.http import Http404, JsonResponse


class LoadMoreView(generic.View):

    def get(self, request, *args, **kwargs):
        if not request.is_ajax():
            raise Http404
        offset = int(self.request.GET.get("offset", ''))
        loadtype = self.request.GET.get("loadtype", '')
        results = []

        if loadtype == "notifications":
            queryset = self.request.user.notifications.all().order_by(
                "-when")[offset:offset + 5]
            for obj in queryset:
                temp = {}
                if str(obj.target_type) == "profile":
                    temp['redirect_id'] = obj.target_id
                    temp['redirect_to'] = "profile/"
                elif str(obj.target_type) == "stream":
                    temp['redirect_id'] = obj.target_object.lobby.id
                    temp['redirect_to'] = "lobby/"
                elif str(obj.target_type) == "report":
                    temp['redirect_id'] = obj.target_object.content_object.lobby.id
                    temp['redirect_to'] = "lobby/"
                elif str(obj.target_type) == "lobby":
                    temp['redirect_id'] = obj.target_id
                    temp['redirect_to'] = "lobby/"
                elif str(obj.target_type) == "lobby membership":
                    temp['redirect_id'] = obj.target_object.lobby.id
                    temp['redirect_to'] = "lobby/"
                elif str(obj.target_type) == "comment":
                    temp['redirect_id'] = obj.target_object.lobby.id
                    temp['redirect_to'] = "lobby/"
                temp['details'] = obj.get_notification
                results.append(temp)

        elif loadtype == "users":
            queryset = User.objects.all()[offset:offset + 5]
            for obj in queryset:
                temp = {}
                temp['username'] = obj.username
                temp['profile_id'] = obj.profile.id
                temp['avatar'] = str(obj.profile.avatar.url)
                results.append(temp)

        elif loadtype == "lobbies":
            queryset = Lobby.objects.all().order_by("-when")[offset:offset + 5]
            for obj in queryset:
                temp = {}
                temp['id'] = obj.id
                if obj.image:
                    temp['image'] = str(obj.image.url)
                else:
                    temp['image'] = "static/images/default_thumbnail.jpg"
                temp['name'] = obj.name
                if obj.owner.profile.avatar:
                    avatar = str(obj.owner.profile.avatar.url)
                else:
                    avatar = "static/images/default_avatar.png"
                temp['owner'] = {
                    'id': obj.owner.id,
                    'username': obj.owner.username,
                    'avatar': avatar,
                    'profile_id': obj.owner.profile.id
                }

                temp['description'] = obj.description
                temp['streams'] = obj.streams.all().count()
                temp['views'] = obj.views.all().count()
                temp['category'] = str(obj.category)
                temp['when'] = obj.when
                results.append(temp)
        # elif loadtype == "favorites":
        #     queryset = self.request.user.favorites.all()[offset:5]
        #     for obj in queryset:
        #         temp = {}
        #         temp['id'] = obj.lobby.id
        #         temp['image'] = obj.lobby.image
        #         temp['name'] = obj.lobby.name
        #         temp['owner'] = {
        #             'id': obj.lobby.owner.id,
        #             'username': obj.lobby.owner.username,
        #             'avatar': obj.lobby.owner.profile.avatar,
        #             'profile_id': obj.lobby.owner.profile.id
        #         }
        #         temp['description'] = obj.lobby.description
        #         temp['streams'] = obj.lobby.streams.all().count()
        #         results.append(temp)
        else:
            print("Error")
        return JsonResponse(
            results, content_type="application/json", safe=False)
