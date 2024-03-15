from .models import Card,UserCard, Decks, DeckCards, TradeRequest, TradeResponse, TradeStatus, OfferedCard, RequestedCard
from django.shortcuts import render

# Create your views here.
def index(request):
    num_cards = Card.objects.all().count()
    num_decks = Decks.objects.count()

    context = {
        'num_cards': num_cards,
        'num_decks': num_decks,
    }

    return render(request, 'index.html', context=context)

