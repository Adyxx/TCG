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

        self.class_trait = None
        if self.main_character and self.main_character.class_type in CLASS_TRAITS:
            self.class_trait = CLASS_TRAITS[self.main_character.class_type]
            self._class_trait_uses_this_turn = 0

        self.hand = []
        self.deck = []
        self.graveyard = []
        self.board = []
        self.cards_played_this_turn = 0
        self.energy = 0

        self.prepare_deck()


    def prepare_deck(self):
        cards = []
        for deck_card in self.deck_model.deck_cards.select_related("card"):
            for _ in range(deck_card.quantity):
                cards.append(GameCard(deck_card.card))
        random.shuffle(cards)
        self.deck = cards

        print(f"📦 Deck for {self.name} prepared with {len(cards)} cards:")
        names = [card.name for card in cards]
        for i, name in enumerate(names, 1):
            print(f"  {i:2}. {name}")

    def draw_card(self):
        if self.deck:
            card = self.deck.pop(0)
            card.owner = self
            self.hand.append(card)
            print(f"🃏 {self.name} drew {card.name}")
        else:
            print(f"⚠️ {self.name}'s deck is empty!")

    def __str__(self):
        return self.name
