from django.db import models
from django.urls import reverse  # Used to generate URLs by reversing the URL patterns
import uuid  # Required for unique ids
from django.contrib.auth.models import User
from datetime import date


class Card(models.Model):
    """Model for: card object - CRUD through game maintenance"""
    card_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                               help_text='Unique ID for this particular card possibility')
    card_title = models.CharField(max_length=30, unique=True, null=False)
    card_description = models.TextField(max_length=100, help_text='Enter a description of the card', null=False)
    card_value = models.IntegerField(null=False)
    card_rules = models.TextField(max_length=500, help_text='Enter the card rules', null=False)

    #   card image = models.??(unique=True, null=True)

    def __str__(self):
        """String representation of the Model object"""
        return self.card_title


class UserCard(models.Model):
    """Model for: Cards belonging to user"""
    user_card_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                    help_text='Unique ID for this card that belongs to user')
    user_card_quantity = models.PositiveIntegerField(null=False)
    player = models.ForeignKey(User, on_delete=models.RESTRICT, null=True)
    card_id = models.ForeignKey('Card', on_delete=models.RESTRICT, null=True)

    def __str__(self):
        """String representation of the Model object"""
        return self.card_id.card_title


class Decks(models.Model):
    """Model for: Decks - creates PK for deck and links to player"""
    decks_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                help_text='Unique ID for this Deck')
    decks_title = models.CharField(max_length=30, null=True)
    player = models.ForeignKey(User, on_delete=models.RESTRICT, null=True)

    def __str__(self):
        """String representation of the Model object"""
        return self.decks_title


class DeckCards(models.Model):
    """Model for: Cards in a Deck - combo key of UserCard & Deck"""
    deck_cards_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                     help_text='Unique ID for this relationship between user cards & decks')
    deck_cards_quantity = models.PositiveIntegerField(null=False)
    decks_id = models.ForeignKey('Decks', on_delete=models.RESTRICT, null=False)
    user_card_id = models.ForeignKey('UserCard', on_delete=models.RESTRICT, null=False)

    def __str__(self):
        """String representation of the Model object"""
        return self.user_card_id.card_id.card_title


class TradeResponse(models.Model):
    """Model for: a trade response"""
    trade_response_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                         help_text='Unique ID for this trade response')
    trade_response_date = models.DateTimeField(null=True)
    playerResponding = models.ForeignKey(User, on_delete=models.RESTRICT, null=True)
    trade_request_id = models.ForeignKey('TradeRequest', on_delete=models.RESTRICT, null=False)

    def __str__(self):
        """String representation of the Model object"""
        return self.trade_response_date


class TradeStatus(models.Model):
    trade_status = models.CharField(max_length=12, unique=True)

    def __str__(self):
        return self.trade_status


class TradeRequest(models.Model):
    """Model for: """
    trade_request_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                        help_text='Unique ID for this trade request')
    trade_request_date = models.DateTimeField(null=True)
    playerRequesting = models.ForeignKey(User, on_delete=models.RESTRICT, null=True)
    STATUS = (
        ('c', 'Cancelled'), ('p', 'Pending'), ('f', 'Finished'),
    )
    status = models.CharField(
        max_length=1,
        choices=STATUS,
        blank=True,
        default='p',
        help_text='Trade Status',
    )


def __str__(self):
    """String representation of the Model object"""
    return self.trade_request_id


class OfferedCard(models.Model):
    """Model for: """
    offered_card_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                       help_text='Unique ID for this Offered Card ')
    offered_card_quantity = models.PositiveIntegerField(null=False)
    trade_request_id = models.ForeignKey('TradeRequest', on_delete=models.RESTRICT, null=False)
    user_card_id = models.ForeignKey('UserCard', on_delete=models.RESTRICT, null=False)

    def __str__(self):
        """String representation of the Model object"""
        return self.user_card_id.card_id.card_title


class RequestedCard(models.Model):
    """Model for: """
    requested_card_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                         help_text='Unique ID for this Requested Card')
    requested_card_quantity = models.PositiveIntegerField(null=False)
    card_id = models.ForeignKey('Card', on_delete=models.RESTRICT, null=False)
    trade_request_id = models.ForeignKey('TradeRequest', on_delete=models.RESTRICT, null=False)

    def __str__(self):
        """String representation of the Model object"""
        return self.card_id.card_title
