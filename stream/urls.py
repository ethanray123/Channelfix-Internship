from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from stream import views, api
app_name = 'stream'

urlpatterns = [
    path('', views.home.HomeView.as_view(), name='home'),
    path('lobbies/',
         views.lobbysearch.LobbySearchView.as_view(), name='lobby_search'),
    path('loadmore/',
         views.loadmore.LoadMoreView.as_view(), name='load_more_content'),
    path('lobby/<int:pk>',
         views.lobby.DetailView.as_view(), name='lobby_detailview'),
    path('managelobby/<int:pk>',
         views.management.DetailView.as_view(), name='manage_detailview'),
    path('managelobby/<int:pk>/edit',
         views.management.LobbyFormView.as_view(), name='lobby_edit'),
    path('managelobby/<int:pk>/remove',
         views.management.RemoveView.as_view(), name='manage_remove'),
    path('managelobby/<int:pk>/moderator',
         views.management.ModeratorView.as_view(), name='manage_moderator'),
    path('managelobby/<int:pk>/tags',
         views.management.TagsView.as_view(), name='manage_tags'),
    path('managelobby/<int:pk>/status',
         views.management.StatusView.as_view(), name='manage_status'),
    path('lobby/<int:pk>/comments/',
         views.lobby.CommentView.as_view(), name='lobby_commentview'),
    path('update_stream/<int:pk>/',
         views.stream.UpdateView.as_view(), name='stream_updateview'),
    path('lobby/<int:pk>/remove_stream/',
         views.stream.RemoveView.as_view(), name='stream_removeview'),
    path('lobby/<int:pk>/create_stream/',
         views.stream.CreateView.as_view(), name='stream_createview'),
    path('lobby/<int:lobby_pk>/publisher/<int:pk>',
         views.stream.PublisherView.as_view(), name='publisher_view'),
    path('lobby/subscribe/',
         views.subscription.SubscribeView.as_view(), name='subscribe'),
    path('profile/<int:pk>',
         views.profile.DetailView.as_view(), name='profile'),
    path('profile/subscribe/',
         csrf_exempt(views.subscription.SubscribeView.as_view()),
         name='subscribe'),
    path('update_profile/<int:pk>/',
         views.profile.UpdateView.as_view(), name='profile_updateview'),
    path('lobby/<int:pk>/request_membership',
         views.lobby.RequestMembershipView.as_view(),
         name='request_membership'),
    path('get_image', views.stream.GetImage.as_view(), name='get_image'),
    path('lobby/<int:pk>/favorite',
         views.lobby.FavoriteView.as_view(), name='favorite_view'),
    # apis
    path('api/stream',
         api.stream.StreamAPI.as_view(), name='api_stream'),
    path('api/lobby',
         api.lobby.LobbyAPI.as_view(), name='api_lobby'),
    path('api/comment',
         api.comment.CommentAPI.as_view(), name='api_comment'),
    path('api/category',
         api.category.CategoryAPI.as_view(), name='api_category'),
    path('api/subscription',
         api.subscription.SubscriptionAPI.as_view(), name='api_subscription'),
    path('api/report',
         api.report.ReportAPI.as_view(), name='api_report'),
    path('api/profile',
         api.profile.ProfileAPI.as_view(), name='api_profile'),
    path('api/moderator',
         api.moderator.ModeratorAPI.as_view(), name='api_moderator'),
    path('api/lobby_views',
         api.lobby_views.LobbyViewsAPI.as_view(), name='api_lobby_views'),
    path('api/lobby_membership',
         api.lobby_membership.LobbyMembershipAPI.as_view(),
         name='api_lobby_membership'),
    path('api/lobby', api.lobby.LobbyAPI.as_view(), name='api_lobby'),
    path('api/search', api.search.SearchAPI.as_view(), name='api_search'),
]
