from backend.engine.game_state import GameState
from backend.engine.actions import play_card, attack, end_turn, start_turn, use_ability, resolve_combat, resolve_damage
from backend.engine.player import Player
from backend.engine.trigger_loader import register_card_triggers, register_player_ability
from backend.registry.effects import draw_card
from django.contrib.auth import get_user_model

User = get_user_model()

def initialize_triggers(player1, player2):
    for player in [player1, player2]:
        if player.main_character:
            if ref := player.main_character.passive_ability_ref:
                register_player_ability(player, "character", ref)
            if ref := player.main_character.solo_bonus_ref:
                if not player.partner_character:
                    register_player_ability(player, "solo", ref)

        if player.partner_character:
            if ref := player.partner_character.partner_ability_ref:
                register_player_ability(player, "partner", ref)

        if ref := player.main_character.class_type:
            register_player_ability(player, "class", ref)

        for card in player.deck + player.hand + player.board:
            register_card_triggers(card, owner=player)

class GameSession:
    def __init__(self, deck1, deck2):
        self.player1 = Player(deck1.user.username, deck1)
        self.player2 = Player(deck2.user.username, deck2)

        self.player1.opponent = self.player2
        self.player2.opponent = self.player1

        initialize_triggers(self.player1, self.player2)

        self.game = GameState([self.player1, self.player2])
        self.current_player = self.game.current_player()

        for p in [self.player1, self.player2]:
            draw_card(source=None, target=p, value=3)
            solo = getattr(p, "solo_bonus", None)
            if solo and solo.get("timing") == "game_start":
                solo["function"](p)

    @property
    def current_opponent(self):
        if self.current_player == self.player1:
            return self.player2
        else:
            return self.player1
        
    def get_hand(self):
        return self.current_player.hand

    def get_board(self):
        return self.current_player.board

    def play_card(self, index):
        return play_card(self.current_player, index)

    def attack(self):
        return attack(self.current_player, self.game.opponent())

    def use_ability(self):
        return use_ability(self.current_player, self.game.opponent())

    def end_turn(self):
        end_turn(self.current_player)
        self.game.turn_index = 1 - self.game.turn_index
        self.current_player = self.game.current_player()
        start_turn(self.current_player)

    def is_game_over(self):
        return self.game.game_over

    def attack_with_card(self, attacker_card, target):
        attacker = attacker_card.owner
        defender = self.current_opponent

        if attacker != self.current_player:
            print("It's not your turn or you don't control this card.")
            return

        if getattr(attacker_card, "tapped", False):
            print("This card is already tapped (attacked this turn).")
            return
        if getattr(attacker_card, "summoning_sickness", True):
            print("This card has summoning sickness and cannot attack yet.")
            return

        resolve_combat(attacker_card, target, attacker, defender)

