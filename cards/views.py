from .models import Card, UserCard, Decks, DeckCards, TradeRequest, TradeResponse, OfferedCard, \
    RequestedCard
from .forms import UserCardForm
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
def index(request):
    """View function for the home page"""
    num_cards = Card.objects.all().count()
    num_decks = Decks.objects.all().count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_cards': num_cards,
        'num_decks': num_decks,
        'num_visits': num_visits,
    }
    # render the HTML template index.html
    # with the data in the context variable
    return render(request, 'index.html', context=context)


class CardRepositoryView(LoginRequiredMixin, generic.ListView):
    model = Card
    template_name = 'cards/card_repository.html'


class CardDetailView(LoginRequiredMixin, generic.DetailView):
    model = Card
    template_name = 'cards/card_detail.html'


class MyCardsListView(LoginRequiredMixin, generic.ListView):
    """generic class-based view list cards owned by logged in user"""
    model = UserCard
    template_name = 'cards/my_cards.html'
    context_object_name = 'my_cards'  # Set the context object name for the queryset
    paginate_by = 10

    def get_queryset(self):
        return UserCard.objects.filter \
            (player=self.request.user)


class MyDecksListView(LoginRequiredMixin, generic.ListView):
    model = UserCard
    template_name = 'cards/my_decks.html'
    paginate_by = 10

    def get_queryset(self):
        return Decks.objects.filter \
            (player=self.request.user).order_by('decks_title')


class TradeRequestListView(LoginRequiredMixin, generic.ListView):
    model = TradeRequest  # Associate the view with the TradeRequest model
    template_name = 'cards/trade_request_list.html'
    context_object_name = 'trade_requests'  # Set the context object name for the queryset

    def get_queryset(self):
        return TradeRequest.objects.all()  # Return all TradeRequest objects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UserCardForm()  # Add the UserCardForm to the context
        return context
