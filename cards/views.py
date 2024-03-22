from .models import Card, UserCard, Decks, DeckCards, TradeRequest, TradeResponse, TradeStatus, OfferedCard, \
    RequestedCard
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
    return render(request, 'index.html', context=context)


class CardListView(LoginRequiredMixin, generic.ListView):
    model = Card


class CardStatsView(LoginRequiredMixin, generic.ListView):
    model = Card
    template_name = 'cards/card_stats.html'


class CardDetailView(LoginRequiredMixin, generic.DetailView):
    model = Card


class CardsByPlayerListView(LoginRequiredMixin, generic.ListView):
    model = UserCard
    template_name = 'cards/my_cards.html'
    paginate_by = 10

    def get_queryset(self):
        return UserCard.objects.filter \
            (player=self.request.user).order_by('card_id')
