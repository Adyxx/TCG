from django.db import models
from .character import Character
from django.core.exceptions import ValidationError

class Card(models.Model):
    RARITY_CHOICES = [
        ("COMMON", "Common"),
        ("RARE", "Rare"),
        ("EPIC", "Epic"),
        ("LEGENDARY", "Legendary"),
    ]

    CARD_TYPE_CHOICES = [
        ("UNIT", "Unit"),  
        ("SPELL", "Spell"),
        ("RITUAL", "Ritual"),
        ("ASSET", "Asset"), 
        # etc.
    ]

    name = models.CharField(max_length=100)
    cost = models.IntegerField()
    rarity = models.CharField(max_length=20, choices=RARITY_CHOICES, default="COMMON")
    card_type = models.CharField(max_length=20, choices=CARD_TYPE_CHOICES)
    color = models.CharField(max_length=20)
    subtype = models.CharField(max_length=50, blank=True)

    power = models.IntegerField(null=True, blank=True)
    health = models.IntegerField(null=True, blank=True)

    is_character_card = models.BooleanField(default=False)
    is_character_exclusive = models.BooleanField(default=False)
    character = models.ForeignKey(Character, null=True, blank=True, on_delete=models.SET_NULL, related_name='cards')

    text = models.TextField(blank=True)

    def clean(self):
        if self.is_character_card and not self.character:
            raise ValidationError("Character card must have a character assigned.")

        if not self.is_character_card and self.is_character_exclusive and not self.character:
            raise ValidationError("Character-exclusive cards must have a character assigned.")

        if not self.is_character_card and self.character and not self.is_character_exclusive:
            raise ValidationError("Non-character cards should not have a character unless marked exclusive.")

        if self.is_character_card and self.card_type != "UNIT":
            raise ValidationError("Character cards must be of type 'UNIT'.")

    def __str__(self):
        return self.name
