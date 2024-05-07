from django.forms import ModelForm
from .models import Decks  # Add import for Card model


class DeckForm(ModelForm):
    class Meta:
        model = Decks
        fields = ['decks_title']
