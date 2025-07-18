# Generated by Django 5.2.3 on 2025-07-13 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0004_characterpairsynergy_characterrelationship'),
    ]

    operations = [
        migrations.AddField(
            model_name='cardeffectbinding',
            name='trigger_zone',
            field=models.CharField(choices=[('board', 'Board'), ('hand', 'Hand'), ('deck', 'Deck'), ('graveyard', 'Graveyard')], default='board', help_text='Zone where this card must be to trigger', max_length=20),
        ),
    ]
