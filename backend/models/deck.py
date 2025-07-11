from django.core.exceptions import ValidationError
from django.db import models
from .users import User
from .character import Character

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

        for deck_card in self.deck_cards.select_related("card__character"):
            card = deck_card.card
            count = deck_card.quantity

            limit = 1 if card.is_character_card else 3

            custom_limit_binding = card.effect_bindings.filter(
                trigger="on_deck_build",
                effect="override_deck_limit"
            ).first()

            if custom_limit_binding:
                try:
                    limit = int(custom_limit_binding.value)
                except (ValueError, TypeError):
                    issues.append(f"Invalid override_deck_limit value on card '{card.name}'")

            card_counts[card.id] = card_counts.get(card.id, 0) + count
            if card_counts[card.id] > limit:
                issues.append(
                    f"{card.name} exceeds allowed limit of {limit} copies."
                )

            if card.is_character_card and card.character:
                cid = card.character.id
                if cid in character_card_tracker:
                    issues.append(
                        f"Multiple character cards for '{card.character.name}' in deck."
                    )
                else:
                    character_card_tracker[cid] = True

        '''
        for deck_card in self.deck_cards.select_related("card__character"):
            card = deck_card.card
            count = deck_card.quantity

            card_counts[card.id] = card_counts.get(card.id, 0) + count

            if card.is_character_card and card.character:
                cid = card.character.id

                if cid in character_card_tracker:
                    issues.append(
                        f"Multiple character cards for '{card.character.name}' in deck."
                    )
                else:
                    character_card_tracker[cid] = True

                if count > 1:
                    issues.append(
                        f"Character card '{card.name}' exceeds the 1-copy limit."
                    )
            else:
                if card_counts[card.id] > 3:
                    issues.append(f"{card.name} exceeds the 3-copy limit.")

        return issues
        '''

    
def clean(self):
    if not self.pk:
        return

    issues = self.get_deck_issues()
    if issues:
        raise ValidationError(issues)

    def __str__(self):
        return f"{self.name} ({self.user.username})"
