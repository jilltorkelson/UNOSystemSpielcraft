# Generated by Django 5.0.3 on 2024-03-14 23:44

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='card_value',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='deckcards',
            name='deck_cards_id',
            field=models.UUIDField(default=uuid.uuid4, help_text='Unique ID for this relationship between user cards & decks', primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='deckcards',
            name='deck_cards_quantity',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='offeredcard',
            name='offered_card_quantity',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='requestedcard',
            name='requested_card_quantity',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='usercard',
            name='user_card_quantity',
            field=models.PositiveIntegerField(),
        ),
    ]