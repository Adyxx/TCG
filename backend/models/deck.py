from django.db import models
from .users import User
from .character import Character

class Deck(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='decks')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    character = models.ForeignKey(Character, null=True, on_delete=models.CASCADE, related_name='main_decks')
    partner_character = models.ForeignKey(Character, null=True, blank=True, on_delete=models.SET_NULL, related_name='partner_decks')

    def __str__(self):
        return f"{self.name} ({self.user.username})"
