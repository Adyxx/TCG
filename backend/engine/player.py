import random
from backend.registry.class_traits import CLASS_TRAITS
from backend.registry.effects import draw_card
from backend.engine.trigger_observer import trigger_observer
from .game_card import GameCard
from backend.engine.trigger_loader import reset_player_abilities

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

        self.cooldowns = {}
        self.turn_usage = {}
        
        if self.main_character:
            class_trait_ref = self.main_character.class_type
            meta = CLASS_TRAITS.get_metadata(class_trait_ref)
            func = CLASS_TRAITS.get_function(class_trait_ref)

            if meta and func:
                self.class_trait = {
                    "name": class_trait_ref,
                    "description": meta["description"],
                    "trigger": meta["trigger"],
                    "condition": meta.get("condition"),
                    "cooldown": meta.get("cooldown"),
                    "function": func,
                }

        self.hand = []
        self.deck = []
        self.graveyard = []
        self.board = []
        self.cards_played_this_turn = 0
        self.turn_count = 0
        self.energy = 0

        self.prepare_deck()


    def prepare_deck(self):
        cards = []
        for deck_card in self.deck_model.deck_cards.select_related("card"):
            for _ in range(deck_card.quantity):
                cards.append(GameCard(deck_card.card))
        random.shuffle(cards)
        self.deck = cards


    def start_turn(self):
        print(f"▶️ {self.name}'s turn begins.")
        self.energy += 1
        print(f"⚡ {self.name} gains 1 energy → {self.energy} total")

        draw_card(self, value=1)

        trigger_observer.emit("turn_started", player=self)

        for card in self.board:
            trigger_observer.emit("turn_started", card=card, player=self)
            card.tapped = False
            card.summoning_sickness = False

        self.turn_count += 1
        self.cards_played_this_turn = 0


    def tick_cooldowns(self):
        for ref in list(self.cooldowns):
            self.cooldowns[ref] = max(0, self.cooldowns[ref] - 1)


    def end_turn(self):
        print(f"⏹ {self.name}'s turn ends.")
        trigger_observer.emit("turn_ended", player=self)

        self.tick_cooldowns()

        ability = getattr(self, "partner_ability", None)
        if ability and ability.get("remaining_cooldown", 0) > 0:
            ability["remaining_cooldown"] -= 1

        for card in self.board:
            trigger_observer.emit("turn_ended", card=card, player=self)
