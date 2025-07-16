import os
import django
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'frontend_web')))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "frontend_web.frontend_web.settings")
django.setup()

from backend.engine.game_state import GameState
from backend.engine.actions import play_card, attack, end_turn, start_turn, use_ability
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

    player1.opponent = player2
    player2.opponent = player1

    initialize_triggers(player1, player2)

    for player in [player1, player2]:
        print(f"\n🧙 {player.name} enters the game!")
        if player.main_character:
            print(f"  🧍 Main Character: {player.main_character.name} (Class: {player.main_character.class_type})")
            if player.class_trait:
                print(f"    🧬 Class Trait: {player.class_trait.get('description', 'No description')}")
            if getattr(player, "solo_bonus", None):
                print(f"    🎁 Solo Bonus: {player.solo_bonus['description']}")
        if player.partner_character:
            print(f"  🧑‍🤝‍🧑 Partner: {player.partner_character.name}")
            if getattr(player, "partner_ability", None):
                partner = player.partner_ability
                if isinstance(partner, dict):
                    print(f"    🔸 Partner Ability: {partner['description']}")
        print(f"  ❤️ Starting Health: {player.health}")
        print(f"  📦 Deck size: {len(player.deck)} cards\n")

    game = GameState([player1, player2])
    current_player = game.current_player()

    for p in [player1, player2]:
        draw_card(source=None, target=p, value=3)

        solo = getattr(p, "solo_bonus", None)
        if solo and solo.get("timing") == "game_start":
            print(f"🎁 {p.name}'s solo bonus activates: {solo['description']}")
            solo["function"](p)


    while not game.game_over:
        print(f"\n=== 🕒 {current_player.name}'s Turn ===")
        start_turn(current_player)

        while True:
            print(f"\n📜 {current_player.name}'s hand:")
            for i, card in enumerate(current_player.hand):
                print(f"  {i}: {card.name} (Cost: {card.cost}, Power: {card.power}, Health: {card.health})")

            print(f"🛡️ Board: {[card.name for card in current_player.board]}")
            command = input(">> Command (play <i> / attack / use / end): ").strip()

            if command.startswith("play"):
                _, idx = command.split()
                play_card(current_player, int(idx))

            elif command == "attack":
                attack(current_player, game.opponent())

            elif command == "end":
                end_turn(current_player)
                game.turn_index = 1 - game.turn_index 
                break

            elif command == "use":
                use_ability(current_player, game.opponent())

            else:
                print("❓ Unknown command.")

        current_player = game.current_player()

if __name__ == "__main__":
    run_game()
