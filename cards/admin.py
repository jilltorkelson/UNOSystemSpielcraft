from django.contrib import admin
from .models import Card,UserCard, Decks, DeckCards, TradeRequest, TradeResponse, TradeStatus, OfferedCard, RequestedCard

# Register your models here.
admin.site.register(Card)
admin.site.register(UserCard)
admin.site.register(Decks)
admin.site.register(DeckCards)
admin.site.register(TradeRequest)
admin.site.register(TradeResponse)
admin.site.register(TradeStatus)
admin.site.register(OfferedCard)
admin.site.register(RequestedCard)