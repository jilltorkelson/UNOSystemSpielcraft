from .models import Card, UserCard, Decks, DeckCards, TradeRequest, TradeResponse, TradeStatus, OfferedCard, \
    RequestedCard
from django.shortcuts import render


# Create your views here.
def index(request):
    """View function for the home page"""
    num_cards = Card.objects.all().count()
    num_decks = Decks.objects.all().count()

    context = {
        'num_cards': num_cards,
        'num_decks': num_decks,
    }
    return render(request, 'index.html', context=context)
