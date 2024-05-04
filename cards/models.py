from django.db import models
from django.urls import reverse  # Used to generate URLs by reversing the URL patterns
from django.core.validators import MinValueValidator  # Import MinValueValidator for validation
import uuid  # Required for unique ids
from django.contrib.auth.models import User


class Card(models.Model):
    """Model for: card object - CRUD through game maintenance"""
    card_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                               help_text='Unique ID for this particular card possibility')
    card_title = models.CharField(max_length=30, unique=True, null=False)
    card_description = models.TextField(max_length=100, help_text='Enter a description of the card', null=False)
    card_value = models.IntegerField(null=False)
    card_rules = models.TextField(max_length=500, help_text='Enter the card rules', null=False)
    card_image = models.ImageField(upload_to='card_images/', null=True, blank=True,
                                   help_text='Upload an image of the card')

    class Meta:
        ordering = ['card_value', 'card_title']

    def get_absolute_url(self):
        """Returns the URL to access a particular card instance."""
        return reverse('card_detail', args=[str(self.card_id)])

    def __str__(self):
        """String representation of the Model object"""
        return f'{self.card_title}'

class UserCard(models.Model):
    """Model for: Cards belonging to user"""
    user_card_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                    help_text='Unique ID for this card that belongs to user')
    user_card_quantity = models.PositiveIntegerField(null=False)
    player = models.ForeignKey(User, on_delete=models.RESTRICT, null=False, blank=False)
    card_id = models.ForeignKey('Card', on_delete=models.RESTRICT, null=True)

    def __str__(self):
        """String representation of the Model object"""
        return f'{self.card_id.card_title}'


class Decks(models.Model):
    """Model for: Decks - creates PK for deck and links to player"""
    decks_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                help_text='Unique ID for this Deck')
    decks_title = models.CharField(max_length=30, null=True)
    player = models.ForeignKey(User, on_delete=models.RESTRICT, null=False, blank=False)

    def __str__(self):
        """String representation of the Model object"""
        return f'{self.decks_title}'


class DeckCards(models.Model):
    """Model for: Cards in a Deck - combo key of UserCard & Deck"""
    deck_cards_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                     help_text='Unique ID for this relationship between user cards & decks')
    deck_cards_quantity = models.PositiveIntegerField(null=False)
    decks_id = models.ForeignKey('Decks', on_delete=models.RESTRICT, null=False)
    user_card_id = models.ForeignKey('UserCard', on_delete=models.RESTRICT, null=False)

    def __str__(self):
        """String representation of the Model object"""
        return f'{self.user_card_id.card_id.card_title}'


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


class TradeRequest(models.Model):
    """Model for: """
    trade_request_date = models.DateTimeField(auto_now_add=True)
    trade_request_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                        help_text='Unique ID for this trade request')
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
        return f'{self.playerRequesting.username} - {self.trade_request_date}'


class OfferedCard(models.Model):
    offered_card_id = models.UUIDField(primary_key=True, default=uuid.uuid4,
                                       help_text='Unique ID for this Offered Card')
    offered_card_quantity = models.PositiveIntegerField(null=False)
    trade_request_id = models.ForeignKey('TradeRequest', on_delete=models.CASCADE, null=False)
    user_card_id = models.ForeignKey('UserCard', on_delete=models.RESTRICT, null=False)

    def __str__(self):
        return f'{self.user_card_id.card_id.card_title}'


class RequestedCard(models.Model):
    requested_card_id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this Requested Card')
    requested_card_quantity = models.PositiveIntegerField(
        default=1,  # Default value (optional)
        validators=[MinValueValidator(1)],  # Ensure the value is at least 1
        help_text='Enter the quantity of requested cards (must be greater than 0)'
    )
    card_id = models.ForeignKey('Card', on_delete=models.RESTRICT, null=False)
    trade_request_id = models.ForeignKey('TradeRequest', on_delete=models.CASCADE, null=True, default=None)

    def __str__(self):
        return f'{self.card_id.card_title}'

    def get_absolute_url(self):
        return reverse('requested_card_detail', args=[str(self.requested_card_id)])