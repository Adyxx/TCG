import os
import django
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'frontend_web')))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "frontend_web.frontend_web.settings")
django.setup()

from backend.engine.game_state import GameState
from backend.engine.player import Player
from backend.engine.actions import play_card, attack, end_turn
from backend.engine.trigger_exec import execute_trigger


def run_game():
    print("🎮 Starting test game...")

    alice = Player("Alice")
    bob = Player("Bob")

    game = GameState([alice, bob])
    current_player = game.current_player()

    while not game.game_over:
        print(f"\n=== 🕒 {current_player.name}'s Turn ===")
        execute_trigger(None, "on_turn_start", current_player)

        while True:
            print(f"\n{current_player.name}'s hand: {[f'{i}: {card.name}' for i, card in enumerate(current_player.hand)]}")
            command = input(">> Command (play <i> / attack / end): ").strip()

            if command.startswith("play"):
                _, idx = command.split()
                play_card(current_player, int(idx))

            elif command == "attack":
                attack(current_player, game.opponent())

            elif command == "end":
                end_turn(game)
                break

            else:
                print("❓ Unknown command.")

        current_player = game.current_player()


if __name__ == "__main__":
    run_game()
