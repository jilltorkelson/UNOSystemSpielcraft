from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_edit_card/', views.AddEditCardView.as_view(), name='add_edit_card'),
    path('add_edit_deck/', views.AddEditDeckView.as_view(), name='add_edit_deck'),
    path('add_edit_usercard/', views.AddEditUserCardView.as_view(), name='add_edit_usercard'),
    path('card_stats/', views.CardStatsView.as_view(), name='card_stats'),
    path('card_repository/', views.CardRepositoryView.as_view(), name='card_repository'),
    path('create_edit_my_trades/', views.CreateEditMyTradesView.as_view(), name='create_edit_my_trades'),
    path('my_cards/', views.MyCardsListView.as_view(), name='my_cards'),
    path('my_decks/', views.MyDecksListView.as_view(), name='my_decks'),
    path('trade_confirmation/', views.TradeConfirmationListView.as_view(), name='trade_confirmation'),
    path('trade_request_list/', views.TradeRequestListView.as_view(), name='trade_request_list'),
    path('reports_dashboard/', views.ReportsDashboardView.as_view(), name='reports_dashboard'),
]
