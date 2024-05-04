from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('card_repository/', views.CardRepositoryView.as_view(), name='card_repository'),
    path('trade_request_list/', views.TradeRequestListView.as_view(), name='trade_request_list'),
    path('my_cards/', views.MyCardsListView.as_view(), name='my_cards'),
    path('my_decks/', views.MyDecksListView.as_view(), name='my_decks'),
    path('card_detail/<int:pk>/', views.CardDetailView.as_view(), name='card_detail'),
    path('my_trade_requests/', views.MyTradeRequestsListView.as_view(), name='my_trade_requests'),
    path('trade_request_create/', views.trade_request_create_view, name='trade_request_create'),
    path('deck_create/', views.deck_create_view, name='deck_create'),
    path('accept_trade_request/<uuid:pk>', views.accept_trade_request_view, name='accept_trade_request')
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
