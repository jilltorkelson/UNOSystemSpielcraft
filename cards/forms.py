from django import forms
from django.forms import ModelForm

from .models import UserCard, Card, Decks  # Add import for Card model


class TradeRequestForm(forms.Form):
    offered_cards = forms.ModelMultipleChoiceField(queryset=UserCard.objects.all(), widget=forms.CheckboxSelectMultiple)
    requested_cards = forms.ModelMultipleChoiceField(queryset=Card.objects.all(), widget=forms.CheckboxSelectMultiple)

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['offered_cards'].queryset = UserCard.objects.filter(player=user)


class DeckForm(ModelForm):
    class Meta:
        model = Decks
        fields = ['decks_title']
