from django import forms
from .models import Game

class CreateGameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ['creator_name', 'rounds', 'scoring_method']
        widgets = {
            'creator_name': forms.TextInput(attrs={'class': 'form-control'}),
            'rounds': forms.Select(attrs={'class': 'form-control'}),
            'scoring_method': forms.Select(attrs={'class': 'form-control'}),
        }

class JoinGameForm(forms.Form):
    player_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    room_code = forms.CharField(max_length=8, widget=forms.TextInput(attrs={'class': 'form-control'}))
