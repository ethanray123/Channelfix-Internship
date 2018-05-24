from django.urls import path
from stream.views import home, lobby, management

app_name = 'stream'

urlpatterns = [
    path('', home.HomeView.as_view(), name='home'),
    path('lobby/<int:pk>',
         lobby.DetailView.as_view(), name='lobby_detailview'),
    path('managelobby/<int:pk>',
         management.DetailView.as_view(), name='manage_detailview'),
    path('managelobby/<int:pk>/edit',
         management.LobbyFormView.as_view(), name='lobby_edit'),
]
