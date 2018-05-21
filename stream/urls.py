from django.urls import path
from stream.views import lobby

urlpatterns = [
    path('lobby/<int:pk>',
         lobby.DetailView.as_view(), name='lobby_detailview'),
]
