from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from .models import Card, UserCard, Decks, TradeRequest, OfferedCard, RequestedCard
from .forms import UserCardForm

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

class CardRepositoryView(LoginRequiredMixin, ListView):
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
        trade_requests = TradeRequest.objects.all()
        form = UserCardForm()
        return render(request, 'cards/trade_request_list.html', {'trade_requests': trade_requests, 'form': form})

    def post(self, request, *args, **kwargs):
        """Handle POST request to process form submission for creating a new trade request"""
        form = UserCardForm(request.POST)
        if form.is_valid():
            new_trade_request = TradeRequest.objects.create(playerRequesting=request.user)
            for card in form.cleaned_data['offered_cards']:
                OfferedCard.objects.create(trade_request_id=new_trade_request, user_card_id=card, offered_card_quantity=1)
            for card in form.cleaned_data['requested_cards']:
                RequestedCard.objects.create(trade_request_id=new_trade_request, card_id=card)
            return redirect('my_trade_requests')

        trade_requests = TradeRequest.objects.all()
        return render(request, 'cards/trade_request_list.html', {'trade_requests': trade_requests, 'form': form})

def trade_request_create_view(request):
    """View function to handle creation of a new trade request"""
    if request.method == 'POST':
        form = UserCardForm(request.POST)
        if form.is_valid():
            offered_cards = form.cleaned_data['offered_cards']
            requested_cards = form.cleaned_data['requested_cards']
            new_trade_request = TradeRequest.objects.create(playerRequesting=request.user)
            for card in offered_cards:
                OfferedCard.objects.create(trade_request_id=new_trade_request, user_card_id=card, offered_card_quantity=1)
            for card in requested_cards:
                RequestedCard.objects.create(trade_request_id=new_trade_request, card_id=card)
            return redirect('my_trade_requests')
    else:
        form = UserCardForm()

    return render(request, 'cards/trade_request_create.html', {'form': form})

class MyTradeRequestsListView(LoginRequiredMixin, View):
    """View to handle displaying and processing trade requests specific to the logged-in user"""
    def get(self, request, *args, **kwargs):
        trade_requests = TradeRequest.objects.filter(playerRequesting=request.user)
        return render(request, 'cards/my_trade_requests.html', {'trade_requests': trade_requests})

    def post(self, request, *args, **kwargs):
        # Handle form submission logic for creating new trade requests
        form = UserCardForm(request.POST)
        if form.is_valid():
            new_trade_request = TradeRequest.objects.create(playerRequesting=request.user)
            for card in form.cleaned_data['offered_cards']:
                new_trade_request.offeredcard_set.create(user_card_id=card, offered_card_quantity=1)
            for card in form.cleaned_data['requested_cards']:
                new_trade_request.requestedcard_set.create(card_id=card, requested_card_quantity=1)
            return redirect('my_trade_requests')

        # If form is invalid, retrieve trade requests and render the template with the form
        trade_requests = TradeRequest.objects.filter(playerRequesting=request.user)
        return render(request, 'cards/my_trade_requests.html', {'trade_requests': trade_requests, 'form': form})