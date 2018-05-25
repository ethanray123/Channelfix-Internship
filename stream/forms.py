from stream.models import Lobby
from django import forms


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
