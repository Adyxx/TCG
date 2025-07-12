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


from django.contrib.auth import get_user_model
from backend.models import DeckCard

User = get_user_model()

def select_user_deck(prompt):
    print(f"\n🔍 {prompt}")
    for user in User.objects.all():
        print(f"👤 {user.id}: {user.username}")
    user_id = int(input("Enter user ID: "))
    user = User.objects.get(id=user_id)

    decks = user.decks.all()
    playable_decks = [d for d in decks if d.is_playable()]
    if not playable_decks:
        print("🚫 No playable decks for this user.")
        exit(1)

    print(f"\n🎴 Playable decks for {user.username}:")
    for i, deck in enumerate(playable_decks):
        print(f"{i}: {deck.name}")
    deck_index = int(input("Choose deck: "))
    return playable_decks[deck_index]


def run_game():
    print("🎮 Starting test game...")

    deck1 = select_user_deck("Select Player 1")
    deck2 = select_user_deck("Select Player 2")

    from backend.engine.player import Player

    player1 = Player(deck1.user.username, deck1)
    player2 = Player(deck2.user.username, deck2)

    # Show full character info
    for player in [player1, player2]:
        print(f"\n🧙 {player.name} enters the game!")
        if player.main_character:
            print(f"  🧍 Main Character: {player.main_character.name} (Class: {player.main_character.class_type})")
            if player.class_trait:
                print(f"    🧬 Class Trait: {player.class_trait.get('description', 'No description')}")
        if player.partner_character:
            print(f"  🧑‍🤝‍🧑 Partner: {player.partner_character.name}")
        print(f"  ❤️ Starting Health: {player.health}")
        print(f"  📦 Deck size: {len(player.deck)} cards\n")

    game = GameState([player1, player2])
    current_player = game.current_player()

    for p in [player1, player2]:
        for _ in range(3):
            p.draw_card()

    while not game.game_over:
        print(f"\n=== 🕒 {current_player.name}'s Turn ===")

        current_player.energy += 1  
        print(f"⚡ {current_player.name} gains 1 energy → {current_player.energy} total")

        current_player.draw_card() 
        execute_trigger(None, "on_turn_start", current_player)
        player._class_trait_uses_this_turn = 0

        for card in current_player.board:
            card.tapped = False
            if card.summoning_sickness:
                card.summoning_sickness = False 

        while True:
            print(f"\n📜 {current_player.name}'s hand:")
            for i, card in enumerate(current_player.hand):
                print(f"  {i}: {card.name} (Cost: {card.cost}, Power: {card.power}, Health: {card.health})")

            print(f"🛡️ Board: {[card.name for card in current_player.board]}")
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
