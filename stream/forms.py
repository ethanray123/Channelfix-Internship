from stream.models import Lobby
from django import forms
from stream import models


class LobbyForm(forms.ModelForm):
    class Meta:
        model = Lobby
        fields = ['name', 'category', 'description']

    def __init__(self, *args, **kwargs):
        super(LobbyForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'autocomplete': 'off',
            })


class StreamForm(forms.ModelForm):
    class Meta:
        model = models.Stream
        fields = ['title', 'URL', 'description', 'image']

    def __init__(self, *args, **kwargs):
        super(StreamForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'autocomplete': 'off',
            })
