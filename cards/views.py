from datetime import datetime

from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import Card, UserCard, Decks, TradeRequest, OfferedCard, RequestedCard, DeckCards, TradeResponse
from .forms import TradeRequestForm, DeckForm
from django.contrib import messages
from django.db import transaction


def index(request):
    """View function for the home page"""
    num_cards = Card.objects.count()
    num_decks = Decks.objects.count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_cards': num_cards,
        'num_decks': num_decks,
        'num_visits': num_visits,
    }
    return render(request, 'index.html', context=context)


class CardRepositoryView(ListView):
    """View for the card repository page"""
    model = Card
    template_name = 'cards/card_repository.html'


class CardDetailView(LoginRequiredMixin, ListView):
    """View for the card detail page"""
    model = Card
    template_name = 'cards/card_detail.html'


class MyCardsListView(LoginRequiredMixin, ListView):
    """View to list cards owned by logged-in user"""
    model = UserCard
    template_name = 'cards/my_cards.html'
    context_object_name = 'my_cards'

    def get_queryset(self):
        return UserCard.objects.filter(player=self.request.user)


class MyDecksListView(LoginRequiredMixin, ListView):
    """View for the my decks page"""
    model = Decks
    template_name = 'cards/my_decks.html'
    context_object_name = 'my_decks'

    def get_queryset(self):
        return Decks.objects.filter(player=self.request.user)


class TradeRequestListView(LoginRequiredMixin, View):
    """View to handle trade requests"""

    def get(self, request, *args, **kwargs):
        """Handle GET request to retrieve and display trade requests"""
        trade_requests = TradeRequest.objects.filter(status='p')
        return render(request, 'cards/trade_request_list.html', {'trade_requests': trade_requests})


def trade_request_create_view(request):
    """View function to handle creation of a new trade request"""
    if request.method == 'POST':
        form = TradeRequestForm(request.POST)
        if form.is_valid():
            offered_cards = form.cleaned_data['offered_cards']
            requested_cards = form.cleaned_data['requested_cards']
            new_trade_request = TradeRequest.objects.create(
                playerRequesting=request.user, trade_request_date=datetime.now())
            for card in offered_cards:
                OfferedCard.objects.create(trade_request_id=new_trade_request, user_card_id=card,
                                           offered_card_quantity=1)
            for card in requested_cards:
                RequestedCard.objects.create(trade_request_id=new_trade_request, card_id=card)
            return redirect('trade_request_list')
    else:
        form = TradeRequestForm(request.user)

    return render(request, 'cards/trade_request_create.html', {'form': form})


def deck_create_view(request):
    """View function to handle creation of a new deck"""
    if request.method == 'POST':
        form = DeckForm(request.POST)
        if form.is_valid():
            deck_cards = form.cleaned_data['deck_cards']
            new_deck = Decks.objects.create(player=request.user, decks_title=form.cleaned_data['title'])
            for card in deck_cards:
                DeckCards.objects.create(decks_id=new_deck, user_card_id=card, deck_cards_quantity=1)
            return redirect('my_decks')
    else:
        form = DeckForm(request.user)
    return render(request, 'cards/deck_create.html', {'form': form})


@transaction.atomic
def accept_trade_request_view(request, pk):
    trade_request = TradeRequest.objects.get(pk=pk)
    try:
        for offered_card in trade_request.offeredcard_set.all():
            current_card = (UserCard.objects.filter(card_id=offered_card.user_card_id.card_id)
                            .filter(player=request.user).first())
            if current_card:
                (UserCard.objects.filter(pk=current_card.user_card_id)
                 .update(user_card_quantity=current_card.user_card_quantity + offered_card.offered_card_quantity))
            else:
                UserCard.objects.create(player=request.user, card_id=offered_card.user_card_id.card_id,
                                        user_card_quantity=offered_card.offered_card_quantity)
            if offered_card.offered_card_quantity >= offered_card.user_card_id.user_card_quantity:
                offered_card.user_card_id.delete()
            else:
                update_card_counts(offered_card.user_card_id, offered_card.offered_card_quantity)
        for requested_card in trade_request.requestedcard_set.all():
            current_card = (UserCard.objects.filter(card_id=requested_card.card_id)
                            .filter(player=trade_request.playerRequesting).first())
            if current_card:
                (UserCard.objects.filter(pk=current_card.user_card_id)
                 .update(user_card_quantity=current_card.user_card_quantity + requested_card.requested_card_quantity))
            else:
                UserCard.objects.create(player=trade_request.playerRequesting, card_id=requested_card.card_id,
                                        user_card_quantity=requested_card.requested_card_quantity)
            card_to_remove = UserCard.objects.filter(player=request.user, card_id=requested_card.card_id).first()
            if requested_card.requested_card_quantity >= card_to_remove.user_card_quantity:
                card_to_remove.delete()
            else:
                update_card_counts(card_to_remove, requested_card.requested_card_quantity)
        TradeResponse.objects.create(trade_response_date=datetime.now(), trade_request_id=trade_request,
                                     playerResponding=request.user)
        TradeRequest.objects.filter(pk=pk).update(status='f')
        messages.success(request, 'trade request accepted')
    except Exception as ex:
        messages.error(request, 'trade request failed')
        return redirect('trade_request_list')
    return redirect('my_cards')


def update_card_counts(user_card_id, quantity):
    quantity_difference = user_card_id.user_card_quantity - quantity
    deck_cards = DeckCards.objects.filter(user_card_id=user_card_id.user_card_id)
    for deck_card in deck_cards:
        if deck_card.deck_cards_quantity > quantity_difference:
            (DeckCards.objects.filter(deck_cards_id=deck_card.deck_cards_id)
             .update(deck_cards_quantity=quantity_difference))
    (UserCard.objects.filter(pk=user_card_id.user_card_id)
     .update(user_card_quantity=quantity_difference))

