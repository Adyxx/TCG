import random
import copy
from backend.models import DeckCard
from backend.registry.class_traits import CLASS_TRAITS
from .game_card import GameCard


class Player:
    def __init__(self, name, deck_model):
        self.name = name
        self.deck_model = deck_model

        self.main_character = getattr(deck_model, "character", None)
        self.partner_character = getattr(deck_model, "partner_character", None)

        self.health = 0
        if self.main_character:
            self.health += self.main_character.solo_hp or 0
        if self.partner_character:
            self.health += self.partner_character.partner_hp or 0
        if self.health == 0:
            self.health = 20 

        if self.main_character and self.main_character.class_type in CLASS_TRAITS:
            trait_data = CLASS_TRAITS[self.main_character.class_type]
            self.class_trait = {
                "name": self.main_character.class_type,
                "description": trait_data["description"],
                "trigger": trait_data["trigger"],
                "uses_per_turn": trait_data["limit_per_turn"],
                "function": trait_data["effect"],
            }
            self._class_trait_uses_this_turn = 0

        self._partner_uses_this_turn = 0
        self._partner_turns_since_reset = 0
        self.hand = []
        self.deck = []
        self.graveyard = []
        self.board = []
        self.cards_played_this_turn = 0
        self.turns_taken = 0
        self.energy = 0

        self.prepare_deck()


    def prepare_deck(self):
        cards = []
        for deck_card in self.deck_model.deck_cards.select_related("card"):
            for _ in range(deck_card.quantity):
                cards.append(GameCard(deck_card.card))
        random.shuffle(cards)
        self.deck = cards
