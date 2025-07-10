from backend.models import Card


class Player:
    def __init__(self, name, health=20):
        self.name = name
        self.health = health
        self.hand = []
        self.deck = list(Card.objects.all()[:5])  # Fake deck
        self.graveyard = []
        self.cards_played_this_turn = 0

        self.draw_starting_hand()

    def draw_starting_hand(self):
        for _ in range(3):
            self.draw_card()

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
