from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('card_list/', views.CardListView.as_view(), name='card_list'),
    path('card_detail/<int:pk>', views.CardDetailView.as_view(), name='card_detail'),
    path('my_cards/', views.CardsByPlayerListView.as_view(), name='my_cards'),
    path('card_stats/', views.CardStatsView.as_view(), name='card_stats')
]
