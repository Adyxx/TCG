from django.db import models
from .deck import Deck
from .card import Card

class DeckCard(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name='deck_cards')
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('deck', 'card')

    def __str__(self):
        return f"{self.quantity}x {self.card.name} in {self.deck.name}"
