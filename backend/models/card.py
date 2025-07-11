from django.db import models
from .character import Character
from django.core.exceptions import ValidationError

class Card(models.Model):
    name = models.CharField(max_length=100)
    cost = models.IntegerField()
    card_type = models.CharField(max_length=50)
    color = models.CharField(max_length=20)
    subtype = models.CharField(max_length=50, blank=True)
    power = models.IntegerField(null=True, blank=True)
    health = models.IntegerField(null=True, blank=True)
    is_character_card = models.BooleanField(default=False)
    character = models.ForeignKey(Character, null=True, blank=True, on_delete=models.SET_NULL, related_name='cards')
    text = models.TextField(blank=True)

    def clean(self):
        if self.is_character_card and not self.character:
            raise ValidationError("Character card must have a character assigned.")
        if not self.is_character_card and self.character:
            raise ValidationError("Non-character cards should not be linked to a character.")

    def __str__(self):
        return self.name
