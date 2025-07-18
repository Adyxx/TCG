from ursina import *

CARD_SCALE = (0.2, 0.3)
FRIENDLY_Y = -0.1
ENEMY_Y = 0.2

class GameBoard(Entity):
    def __init__(self, session, parent=None, combat_ui=None, **kwargs):
        if parent is None:
            parent = camera.ui
        super().__init__(parent=parent, **kwargs)
        self.session = session
        self.combat_ui = combat_ui

        self.friendly_cards = []
        self.enemy_cards = []

        self.update_board()

    def update_board(self):
        total_cards = len(self.session.current_player.board) + len(self.session.current_opponent.board)
        total_buttons = len(self.friendly_cards) + len(self.enemy_cards)

        for btn in self.friendly_cards + self.enemy_cards:
            btn.enabled = False

        for i, card in enumerate(self.session.current_player.board):
            if i < len(self.friendly_cards):
                btn = self.friendly_cards[i]
                btn.enabled = True
            else:
                btn = self.create_card_entity(card, i, FRIENDLY_Y, friendly=True)
                self.friendly_cards.append(btn)
            btn.text = f"{card.name}\n{card.power}/{card.health - card.damage_taken}"
            btn.position = (-0.6 + i * 0.25, FRIENDLY_Y)
            card.ui_entity = btn

        for j in range(len(self.session.current_player.board), len(self.friendly_cards)):
            self.friendly_cards[j].enabled = False

        for i, card in enumerate(self.session.current_opponent.board):
            if i < len(self.enemy_cards):
                btn = self.enemy_cards[i]
                btn.enabled = True
            else:
                btn = self.create_card_entity(card, i, ENEMY_Y, friendly=False)
                self.enemy_cards.append(btn)
            btn.text = f"{card.name}\n{card.power}/{card.health - card.damage_taken}"
            btn.position = (-0.6 + i * 0.25, ENEMY_Y)
            card.ui_entity = btn

        for j in range(len(self.session.current_opponent.board), len(self.enemy_cards)):
            self.enemy_cards[j].enabled = False
            
    def create_card_entity(self, card, index, y, friendly):
        x = -0.6 + index * 0.25
        btn = Button(
            text=f"{card.name}\n{card.power}/{card.health - card.damage_taken}",
            scale=CARD_SCALE,
            position=(x, y),
            parent=self,
            color=color.azure if friendly else color.white
        )
        if friendly:
            btn.on_click = Func(self.combat_ui.on_friendly_card_clicked, card)
        return btn
