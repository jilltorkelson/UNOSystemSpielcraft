from datetime import datetime

from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView
from .models import Card, UserCard, Decks, TradeRequest, OfferedCard, RequestedCard, DeckCards, TradeResponse
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
        user_cards = UserCard.objects.filter(player=self.request.user)
        available_trades = []
        for trade_request in trade_requests:
            all_found = True
            for requested_card in trade_request.requestedcard_set.all():
                found_one = False
                for user_card in user_cards:
                    if (user_card.card_id == requested_card.card_id
                            and user_card.user_card_quantity >= requested_card.requested_card_quantity):
                        found_one = True
                if not found_one:
                    all_found = False
            if all_found:
                available_trades.append(trade_request.trade_request_id)
        return render(request, 'cards/trade_request_list.html',
                      {'trade_requests': trade_requests, 'available_trades': available_trades})


class TradeRequestCreateView(LoginRequiredMixin, CreateView):
    model = TradeRequest
    template_name = 'cards/trade_request_create.html'
    fields = []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_cards'] = UserCard.objects.filter(player=self.request.user)
        context['cards'] = Card.objects.all()
        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = request.POST
        trade_request = TradeRequest.objects.create(playerRequesting=self.request.user)
        user_cards = UserCard.objects.filter(player=self.request.user)
        cards = Card.objects.all()
        for user_card in user_cards:
            form_id = 'id_' + user_card.user_card_id.__str__()
            if form[form_id] and int(form[form_id]) > 0:
                quantity = int(form[form_id])
                OfferedCard.objects.create(offered_card_quantity=quantity, trade_request_id=trade_request,
                                           card_id=user_card.card_id)
                if user_card.user_card_quantity == quantity:
                    UserCard.objects.filter(pk=user_card.pk).delete()
                else:
                    update_card_counts(user_card, quantity)
        for card in cards:
            form_id = 'id_' + card.card_id.__str__()
            if form[form_id] and int(form[form_id]) > 0:
                RequestedCard.objects.create(requested_card_quantity=form[form_id], card_id=card,
                                             trade_request_id=trade_request)
        return redirect('trade_request_list')


class DeckCreateView(LoginRequiredMixin, CreateView):
    model = Decks
    template_name = 'cards/deck_create.html'
    fields = []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_cards = UserCard.objects.filter(player=self.request.user)
        return_cards = []
        if 'pk' in self.kwargs:
            deck = Decks.objects.filter(pk=self.kwargs['pk']).first()
            context['id_deck_id'] = deck
            for user_card in user_cards:
                deck_card = deck.deckcards_set.filter(user_card_id=user_card.user_card_id).first()
                if deck_card:
                    return_cards.append((user_card, deck_card.deck_cards_quantity))
                else:
                    return_cards.append((user_card, 0))
        else:
            for user_card in user_cards:
                return_cards.append((user_card, 0))
        context['user_cards'] = return_cards
        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = request.POST
        if form['id_deck_id']:
            Decks.objects.get(pk=form['id_deck_id']).delete()
        deck = Decks.objects.create(decks_title=form['decks_title'], player=self.request.user)
        user_cards = UserCard.objects.filter(player=self.request.user)
        for user_card in user_cards:
            form_id = 'id_' + user_card.user_card_id.__str__()
            if form[form_id] and int(form[form_id]) > 0:
                DeckCards.objects.create(deck_cards_quantity=form[form_id], decks_id=deck, user_card_id=user_card)
        return redirect('my_decks')


def delete_deck_view(request, pk):
    deck = Decks.objects.get(pk=pk)
    deck.delete()
    return redirect('my_decks')


@transaction.atomic
def accept_trade_request_view(request, pk):
    trade_request = TradeRequest.objects.get(pk=pk)
    try:
        for offered_card in trade_request.offeredcard_set.all():
            handle_new_cards(offered_card.card_id, request.user,
                             offered_card.offered_card_quantity)

        for requested_card in trade_request.requestedcard_set.all():
            handle_new_cards(requested_card.card_id, trade_request.playerRequesting,
                             requested_card.requested_card_quantity)

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


def handle_new_cards(card_id, user, quantity):
    current_card = (UserCard.objects.filter(card_id=card_id)
                    .filter(player=user).first())
    if current_card:
        (UserCard.objects.filter(pk=current_card.user_card_id)
         .update(user_card_quantity=current_card.user_card_quantity + quantity))
    else:
        UserCard.objects.create(player=user, card_id=card_id, user_card_quantity=quantity)
