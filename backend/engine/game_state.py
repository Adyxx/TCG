class GameState:
    def __init__(self, players):
        self.players = players
        self.turn_index = 0
        self.game_over = False

    def current_player(self):
        return self.players[self.turn_index]

    def opponent(self):
        return self.players[1 - self.turn_index]
