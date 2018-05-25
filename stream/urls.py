from django.urls import path
from stream.views import lobby

app_name = 'stream'

urlpatterns = [
    path('lobby/<int:pk>',
         lobby.DetailView.as_view(), name='lobby_detailview'),
    path('lobby/<int:pk>/comments/',
         lobby.CommentView.as_view(), name='lobby_commentview'),
]
