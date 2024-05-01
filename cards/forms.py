from django import forms
from .models import UserCard, Card  # Add import for Card model
from .models import TradeRequest
class UserCardForm(forms.Form):
    offered_cards = forms.ModelMultipleChoiceField(queryset=UserCard.objects.all(), widget=forms.CheckboxSelectMultiple)
    requested_cards = forms.ModelMultipleChoiceField(queryset=Card.objects.all(), widget=forms.CheckboxSelectMultiple)