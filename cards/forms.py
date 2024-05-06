from django import forms
from .models import UserCard, Card  # Add import for Card model


class TradeRequestForm(forms.Form):
    # TODO: Filter to only current users cards
    offered_cards = forms.ModelMultipleChoiceField(queryset=UserCard.objects.all(), widget=forms.CheckboxSelectMultiple)
    requested_cards = forms.ModelMultipleChoiceField(queryset=Card.objects.all(), widget=forms.CheckboxSelectMultiple)


class DeckForm(forms.Form):
    # TODO: Filter to only current users cards
    deck_cards = forms.ModelMultipleChoiceField(queryset=UserCard.objects.all(), widget=forms.CheckboxSelectMultiple)
    title = forms.CharField(widget=forms.TextInput)
