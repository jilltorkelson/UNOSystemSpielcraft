from django import forms
from .models import UserCard, Card  # Add import for Card model


class TradeRequestForm(forms.Form):
    offered_cards = forms.ModelMultipleChoiceField(queryset=UserCard.objects.all(), widget=forms.CheckboxSelectMultiple)
    requested_cards = forms.ModelMultipleChoiceField(queryset=Card.objects.all(), widget=forms.CheckboxSelectMultiple)

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['offered_cards'].queryset = UserCard.objects.filter(player=user)


class DeckForm(forms.Form):
    deck_cards = forms.ModelMultipleChoiceField(queryset=UserCard.objects.all(), widget=forms.CheckboxSelectMultiple)
    title = forms.CharField(widget=forms.TextInput)

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['deck_cards'].queryset = UserCard.objects.filter(player=user)
