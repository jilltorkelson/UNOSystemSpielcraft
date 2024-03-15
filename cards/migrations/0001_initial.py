# Generated by Django 5.0.3 on 2024-03-14 23:18

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Card',
            fields=[
                ('card_id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this particular card possibility', primary_key=True, serialize=False)),
                ('card_title', models.CharField(max_length=30, unique=True)),
                ('card_description', models.TextField(help_text='Enter a description of the card', max_length=100)),
                ('card_value', models.IntegerField(max_length=7)),
                ('card_rules', models.TextField(help_text='Enter the card rules', max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Decks',
            fields=[
                ('decks_id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this Deck', primary_key=True, serialize=False)),
                ('decks_title', models.CharField(max_length=30, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TradeRequest',
            fields=[
                ('trade_request_id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this trade request', primary_key=True, serialize=False)),
                ('trade_request_date', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TradeStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trade_status', models.CharField(max_length=12, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='RequestedCard',
            fields=[
                ('requested_card_id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this Requested Card', primary_key=True, serialize=False)),
                ('requested_card_quantity', models.PositiveIntegerField(max_length=6)),
                ('card_id', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='cards.card')),
                ('trade_request_id', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='cards.traderequest')),
            ],
        ),
        migrations.CreateModel(
            name='TradeResponse',
            fields=[
                ('trade_response_id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this trade response', primary_key=True, serialize=False)),
                ('trade_response_date', models.DateTimeField(null=True)),
                ('trade_request_id', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='cards.traderequest')),
            ],
        ),
        migrations.AddField(
            model_name='traderequest',
            name='trade_request_status',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='cards.tradestatus'),
        ),
        migrations.CreateModel(
            name='UserCard',
            fields=[
                ('user_card_id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this card that belongs to user', primary_key=True, serialize=False)),
                ('user_card_quantity', models.PositiveIntegerField(max_length=6)),
                ('card_id', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='cards.card')),
            ],
        ),
        migrations.CreateModel(
            name='OfferedCard',
            fields=[
                ('offered_card_id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this Offered Card ', primary_key=True, serialize=False)),
                ('offered_card_quantity', models.PositiveIntegerField(max_length=6)),
                ('trade_request_id', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='cards.traderequest')),
                ('user_card_id', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='cards.usercard')),
            ],
        ),
        migrations.CreateModel(
            name='DeckCards',
            fields=[
                ('deck_cards_id', models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this relationship between usercards & decks', primary_key=True, serialize=False)),
                ('deck_cards_quantity', models.PositiveIntegerField(max_length=6)),
                ('decks_id', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='cards.decks')),
                ('user_card_id', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='cards.usercard')),
            ],
        ),
    ]
