from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_edit_cards/', views.AddEditCardView.as_view(), name='add_edit_cards'),
    path('add_edit_deck/', views.AddEditDeckView.as_view(), name='add_edit_deck'),
    path('add_edit_usercards/', views.AddEditUserCardView.as_view(), name='add_edit_usercards'),
    path('admin_main/', views.AdminMainView.as_view(), name='admin_main'),
    path('card_stats/', views.CardStatsView.as_view(), name='card_stats'),
    path('create_edit_my_trades/', views.CreateEditMyTradesView.as_view(), name='create_edit_my_trades'),
    path('edit_card/', views.EditCardView.as_view(), name='edit_card'),
    path('edit_deck/', views.EditDeckView.as_view(), name='edit_deck'),
    path('my_cards/', views.MyCardsListView.as_view(), name='my_cards'),
    path('my_decks/', views.MyDecksListView.as_view(), name='my_decks'),
    path('reports_dashboard/', views.ReportsDashboardView.as_view(), name='reports_dashboard'),
    path('trade_confirmation/', views.TradeConfirmationListView.as_view(), name='trade_confirmation'),
    path('trade_request_list/', views.TradeRequestListView.as_view(), name='trade_request_list'),

]
