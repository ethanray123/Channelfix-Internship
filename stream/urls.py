from django.urls import path
from stream.views import home, lobby, management, stream, subscription
app_name = 'stream'

urlpatterns = [
    path('', home.HomeView.as_view(), name='home'),
    path('lobby/<int:pk>',
         lobby.DetailView.as_view(), name='lobby_detailview'),
    path('managelobby/<int:pk>',
         management.DetailView.as_view(), name='manage_detailview'),
    path('managelobby/<int:pk>/edit',
         management.LobbyFormView.as_view(), name='lobby_edit'),
    path('managelobby/<int:pk>/remove',
         management.RemoveView.as_view(), name='manage_remove'),
    path('managelobby/<int:pk>/tags',
         management.TagsView.as_view(), name='manage_tags'),
    path('lobby/<int:pk>/comments/',
         lobby.CommentView.as_view(), name='lobby_commentview'),
    path('update_stream/<int:pk>/',
         stream.UpdateView.as_view(), name='stream_updateview'),
    path('delete_stream/<int:pk>/',
         stream.DeleteView.as_view(), name='stream_deleteview'),
    path('lobby/<int:pk>/create_stream/',
         stream.CreateView.as_view(), name='stream_createview'),
    path('lobby/subscribe/',
         subscription.SubscribeView.as_view(), name='subscribe'),
    path('lobby/<int:pk>/join_lobby',
         lobby.JoinView.as_view(), name='join_lobby'),
]
