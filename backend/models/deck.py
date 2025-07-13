from django.core.exceptions import ValidationError
from django.db import models
from .users import User
from .character import Character
from backend.registry.effects import EFFECT_REGISTRY

class Deck(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='decks')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    character = models.ForeignKey(Character, null=True, on_delete=models.CASCADE, related_name='main_decks')
    partner_character = models.ForeignKey(Character, null=True, blank=True, on_delete=models.SET_NULL, related_name='partner_decks')

    def total_card_count(self):
        return sum(dc.quantity for dc in self.deck_cards.all())

    def is_playable(self):
        return not self.get_deck_issues()

    def get_deck_issues(self):
        issues = []

        if self.total_card_count() < 40:
            issues.append("Deck has fewer than 40 cards.")

        card_counts = {}
        character_card_tracker = {}
        character_card_found = set()

        for deck_card in self.deck_cards.select_related("card__character"):
            card = deck_card.card
            count = deck_card.quantity

            limit = 1 if card.is_character_card else 3

            for binding in card.effect_bindings.filter(trigger__script_reference="on_deck_build"):
                effect_name = binding.effect.script_reference
                if effect_name == "override_deck_limit":
                    try:
                        new_limit = int(binding.value)
                        effect_meta = EFFECT_REGISTRY.get(effect_name)
                        if effect_meta:
                            func = effect_meta["func"]
                            func(card, new_limit)
                            limit = getattr(card, 'override_limit', limit)
                    except (ValueError, TypeError):
                        issues.append(f"Invalid override_deck_limit value on card '{card.name}'")


            card_counts[card.id] = card_counts.get(card.id, 0) + count
            if card_counts[card.id] > limit:
                issues.append(f"{card.name} exceeds allowed limit of {limit} copies.")

            if card.is_character_card and card.character:
                cid = card.character.id
                if cid in character_card_tracker:
                    issues.append(f"Multiple character cards for '{card.character.name}' in deck.")
                else:
                    character_card_tracker[cid] = True
                    character_card_found.add(cid)

        if self.character and self.character.id not in character_card_found:
            issues.append(f"Deck is missing character card for '{self.character.name}'.")

        if self.partner_character and self.partner_character.id not in character_card_found:
            issues.append(f"Deck is missing character card for partner '{self.partner_character.name}'.")

        return issues

    def clean(self):
        pass

    def __str__(self):
        return f"{self.name} ({self.user.username})"

