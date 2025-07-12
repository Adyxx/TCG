class GameCard:
    def __init__(self, card_model):
        self.model = card_model 

        self.name = card_model.name
        self.cost = card_model.cost
        self.power = card_model.power
        self.health = card_model.health

        self.owner = None
        self.zone = None  # "hand", "board", "graveyard", etc.
        self.summoning_sickness = True
        self.tapped = False
        self.temp_buffs = []
        self.damage_taken = 0

    def __getattr__(self, item):
        return getattr(self.model, item)

    def __repr__(self):
        return f"<GameCard {self.name} (Cost: {self.cost}, Power: {self.power}, Health: {self.health})>"
