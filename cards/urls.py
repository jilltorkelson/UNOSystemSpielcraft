from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('assign_cards/', views.AssignCardsListView.as_view(), name='assign_cards'),
    path('card_detail/<int:pk>', views.CardDetailView.as_view(), name='card_detail'),
    path('card_list/', views.CardListView.as_view(), name='card_list'),path('card_stats/', views.CardStatsView.as_view(), name='card_stats'),
    path('card_stats/', views.CardStatsView.as_view(), name='card_stats'),
    path('deck_detail/<int:pk>', views.DecksDetailView.as_view(), name='deck_detail'),
    path('deck_list/', views.DecksListView.as_view(), name='deck_list'),
    #The main screen for maintenance listing all tables - cards, users, etc.
    path('maintenance_main/', views.MaintenanceMainListView.as_view(), name='maintenance_main'),
    path('my_cards/', views.MyCardsListView.as_view(), name='my_cards'),
    path('my_decks/', views.MyDecksListView.as_view(), name='my_decks'),
    path('my_trades/', views.MyTradesListView.as_view(), name='my_trades'),
    path('player_home/', views.PlayerHomeListView.as_view(), name='player_home'),
    path('reports_dashboard/', views.ReportsDashboardView.as_view(), name='reports_dashboard'),
    path('trade_confirmation/', views.TradeConfirmationListView.as_view(), name='trade_confirmation'),
    path('trade_request_list/', views.TradeRequestListView.as_view(), name='trade_request_list'),
    path('user_list/', views.UserListView.as_view(), name='user_list'),

    ]
