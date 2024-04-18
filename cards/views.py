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
    # render the HTML template index.html
    # with the data in the context variable
    return render(request, 'index.html', context=context)


class AssignCardsListView(LoginRequiredMixin, generic.DetailView):
    model = UserCard
    template_name = 'cards/UserCards_AddEdit.html'


class CardListView(LoginRequiredMixin, generic.ListView):
    model = Card
    template_name = 'cards/card_list.html'


class CardStatsView(LoginRequiredMixin, generic.ListView):
    model = Card
    template_name = 'cards/card_stats.html'


class DecksDetailView(LoginRequiredMixin, generic.DetailView):
    model = Card
    template_name = 'cards/deck_add_edit.html'


class DecksListView(LoginRequiredMixin, generic.ListView):
    model = Card
    template_name = 'cards/deck_list.html'


class MaintenanceMainListView(LoginRequiredMixin, generic.ListView):
    model = UserCard
    template_name = 'cards/maintenance_main.html'
    paginate_by = 10


class MyCardsListView(LoginRequiredMixin, generic.ListView):
    model = UserCard
    template_name = 'cards/my_cards.html'
    paginate_by = 10

    def get_queryset(self):
        return UserCard.objects.filter \
            (player=self.request.user).order_by('card_id')


class MyDecksListView(LoginRequiredMixin, generic.ListView):
    model = UserCard
    template_name = 'cards/my_decks.html'
    paginate_by = 10

    def get_queryset(self):
        return UserCard.objects.filter \
            (player=self.request.user).order_by('card_id')


class MyTradesListView(LoginRequiredMixin, generic.ListView):
    model = UserCard
    template_name = 'cards/my_trades.html'
    paginate_by = 10

    def get_queryset(self):
        return UserCard.objects.filter \
            (player=self.request.user).order_by('card_id')


class PlayerHomeListView(LoginRequiredMixin, generic.ListView):
    model = Card
    template_name = 'cards/player_home.html'


class ReportsDashboardView(LoginRequiredMixin, generic.ListView):
    model = Card
    template_name = 'cards/reports_dashboard.html'


class TradeConfirmationListView(LoginRequiredMixin, generic.ListView):
    model = Card
    template_name = 'cards/trade_confirmation.html'


class TradeRequestListView(LoginRequiredMixin, generic.ListView):
    model = Card
    template_name = 'cards/trade_request_list.html'


class UserListView(LoginRequiredMixin, generic.ListView):
    model = UserCard
    template_name = 'cards/user_list.html'


class CardDetailView(LoginRequiredMixin, generic.DetailView):
    model = Card
    template_name = 'cards/card_detail.html'