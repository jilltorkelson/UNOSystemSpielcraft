# Generated by Django 4.2.11 on 2024-04-28 21:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0007_alter_decks_player_alter_usercard_player'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestedcard',
            name='trade_request_id',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.RESTRICT, to='cards.traderequest'),
        ),
    ]
