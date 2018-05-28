from django.urls import path
from stream.views import home, lobby, management, subscription

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
    path('lobby/<int:pk>/comments/',
         lobby.CommentView.as_view(), name='lobby_commentview'),
    path('lobby/subscribe/',
         subscription.SubscribeView.as_view(), name='subscribe'),
]
