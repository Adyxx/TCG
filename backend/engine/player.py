import random
from backend.models import Card, DeckCard

class Player:
    def __init__(self, name, deck_model):
        self.name = name
        self.health = 20
        self.hand = []
        self.deck = []
        self.graveyard = []
        self.board = []
        self.cards_played_this_turn = 0
        self.energy = 0
        self.deck_model = deck_model

        self.prepare_deck()

    def prepare_deck(self):
        cards = []
        for deck_card in self.deck_model.deck_cards.select_related("card"):
            cards.extend([deck_card.card] * deck_card.quantity)
        random.shuffle(cards)
        self.deck = cards

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
