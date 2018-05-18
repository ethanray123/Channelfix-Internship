from django.contrib import admin
from .models import *
# Register your models here.


class ListProfiles(admin.ModelAdmin):
    list_display = ('owner', 'nickname')
    list_filter = ['owner']


class ListModerators(admin.ModelAdmin):
    list_display = ('owner', 'lobby')
    list_filter = ['owner']


class ListComments(admin.ModelAdmin):
    list_display = ('owner', 'lobby', 'when')
    list_filter = ['when']


class ListMembership(admin.ModelAdmin):
    list_display = ('member', 'lobby')
    list_filter = ['lobby']


admin.site.register(Category)
admin.site.register(Profile, ListProfiles)
admin.site.register(Lobby)
admin.site.register(Moderator, ListModerators)
admin.site.register(Stream)
admin.site.register(Comment, ListComments)
admin.site.register(Lobby_Membership, ListMembership)
