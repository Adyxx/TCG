from ursina import *
from ursina.prefabs.health_bar import HealthBar
from collections.abc import Sequence
from backend.engine.actions import get_targets
from .game_board import GameBoard
from .targeting_ui import visual_target_selector

class CombatUI(Entity):
    def __init__(self, session, exit_callback, **kwargs):
        super().__init__(parent=camera.ui, **kwargs)
        self.session = session
        self.exit_callback = exit_callback

        self.player_health = HealthBar(parent=self, position=(-0.6, 0.4), scale=(0.4, 0.05))
        self.opponent_health = HealthBar(parent=self, position=(0.6, 0.4), scale=(0.4, 0.05))

        self.hand_card_buttons = []
        self.hand_panel = Entity(parent=self, y=-0.45)
        self.render_hand()

        self.game_board = GameBoard(session=self.session, parent=self, combat_ui=self)

        self.end_turn_btn = Button(
            text="End Turn",
            on_click=self.end_turn,
            position=(0.4, 0.35),
            scale=(0.2, 0.1),
            parent=self
        )

        self.leave_btn = Button(
            text="Leave",
            on_click=self.exit_callback,
            position=(0.7, -0.45),
            scale=(0.15, 0.08),
            parent=self
        )

        self.selected_card = None

        self.update_health()

    def update_health(self):
        self.player_health.value = self.session.current_player.health
        self.opponent_health.value = self.session.current_opponent.health

    def render_hand(self):
        for b in self.hand_card_buttons:
            b.disable()
            b.parent = None
        self.hand_card_buttons.clear()

        for i, card in enumerate(self.session.get_hand()):
            b = Button(
                text=card.name,
                on_click=lambda i=i: self.play_card(i),
                position=(-0.6 + i * 0.25, 0),
                scale=(0.2, 0.3),
                parent=self.hand_panel
            )
            self.hand_card_buttons.append(b)

    def play_card(self, index):
        self.session.play_card(index)
        self.render_hand()
        self.game_board.update_board()
        self.update_health()

    def end_turn(self):
        self.session.end_turn()
        self.render_hand()
        self.game_board.update_board()
        self.update_health()

    def on_friendly_card_clicked(self, card):
        if self.selected_card:
            print("Already selecting a card to attack with.")
            return
        self.selected_card = card
        print(f"Selected attacker: {card.name}")

        valid_targets = [self.session.current_opponent] + self.session.current_opponent.board
        self.prompt_target_selection(valid_targets)

    def prompt_target_selection(self, targets: Sequence):
        if not targets:
            print("No valid targets.")
            self.selected_card = None
            return

        def on_chosen_target(target):
            print(f"Target chosen: {target}")
            self.session.attack_with_card(self.selected_card, target)

            self.selected_card = None
            self.game_board.update_board()
            self.update_health()
            self.clear_target_buttons()

        visual_target_selector(targets, on_chosen_target)

    def clear_target_buttons(self):
        pass
