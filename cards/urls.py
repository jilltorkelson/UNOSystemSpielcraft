from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('card_repository/', views.CardRepositoryView.as_view(), name='card_repository'),
    path('trade_request_list/', views.MyTradeRequestsView.as_view(), name='trade_request_list'),
    path('my_cards/', views.MyCardsListView.as_view(), name='my_cards'),
    path('my_decks/', views.MyDecksListView.as_view(), name='my_decks'),
    path('card_detail/<int:pk>', views.CardDetailView.as_view(), name='card_detail'),
]
