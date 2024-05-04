from django import forms
from .models import UserCard, Card  # Add import for Card model


class UserCardForm(forms.Form):
    offered_cards = forms.ModelMultipleChoiceField(queryset=UserCard.objects.all(), widget=forms.CheckboxSelectMultiple)
    requested_cards = forms.ModelMultipleChoiceField(queryset=Card.objects.all(), widget=forms.CheckboxSelectMultiple)
