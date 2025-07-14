import os
import django
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'frontend_web')))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "frontend_web.frontend_web.settings")
django.setup()

from backend.engine.game_state import GameState
from backend.engine.actions import play_card, attack, end_turn, start_turn, choose_target
from backend.engine.trigger_loader import register_card_triggers
from backend.registry.effects import draw_card
from django.contrib.auth import get_user_model

User = get_user_model()

from backend.registry.class_traits import CLASS_TRAITS
from backend.engine.trigger_observer import trigger_observer

from backend.registry.character_abilities import CHARACTER_ABILITY_METADATA, CHARACTER_ABILITY_REGISTRY


from backend.registry.triggers import TRIGGER_REGISTRY

def register_passive_ability(player):
    player._passive_uses_this_turn = 0

    ref = player.main_character.passive_ability_ref
    if not ref:
        return

    meta = CHARACTER_ABILITY_METADATA.get(ref)
    func = CHARACTER_ABILITY_REGISTRY.get(ref)

    if not meta or not func or meta["type"] != "passive":
        print(f"⚠️ {ref} is not a valid passive ability.")
        return

    trigger_code = meta.get("trigger")
    limit = meta.get("limit_per_turn")
    if limit is None:
        limit = 999


    trigger_meta = TRIGGER_REGISTRY.get(trigger_code)
    if not trigger_meta:
        print(f"❌ Unknown trigger code '{trigger_code}' for passive '{ref}'")
        return

    event_name = trigger_meta["event"]
    if not event_name:
        print(f"⏭️ Passive ability '{ref}' uses trigger '{trigger_code}', which has no runtime event.")
        return

    def wrapped(**kwargs):
        if player._passive_uses_this_turn >= limit:
            print(f"🚫 {player.name}'s passive '{ref}' limit reached.")
            return

        print(f"✨ Passive ability '{ref}' triggered for {player.name}!")
        func(player)
        player._passive_uses_this_turn += 1

    trigger_observer.subscribe(event_name, wrapped)
    player.passive_ability = meta
    print(f"🧠 Registered passive '{ref}' for {player.name} (event: {event_name})")

def register_class_trait(player):
    player._class_trait_uses_this_turn = 0

    trait = CLASS_TRAITS.get(player.main_character.class_type)
    if not trait:
        print(f"❌ No class trait found for class: {player.main_character.class_type}")
        return

    trigger_code = trait.get("trigger")
    limit = trait.get("limit_per_turn")
    effect = trait.get("effect")

    if not trigger_code or not effect:
        print(f"⏭️ Skipping invalid class trait for {player.name}")
        return

    trigger_meta = TRIGGER_REGISTRY.get(trigger_code)
    if not trigger_meta:
        print(f"❌ Unknown trigger code '{trigger_code}' for class trait")
        return

    event_name = trigger_meta["event"]
    if not event_name:
        print(f"⏭️ Class trait uses trigger '{trigger_code}', which has no runtime event.")
        return

    def wrapped_effect(**kwargs):
        if player._class_trait_uses_this_turn >= limit:
            print(f"🚫 {player.name}'s class trait limit reached this turn.")
            return

        print(f"🧬 {player.name}'s class trait activated!")

        effect(player)
        player._class_trait_uses_this_turn += 1

    trigger_observer.subscribe(event_name, wrapped_effect)
    player.class_trait = trait
    print(f"🔧 Registered class trait for {player.name} (event: {event_name})")


def initialize_triggers(player1, player2):
    for player in [player1, player2]:
        register_class_trait(player)
        register_passive_ability(player)
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
        if player.partner_character:
            print(f"  🧑‍🤝‍🧑 Partner: {player.partner_character.name}")
        print(f"  ❤️ Starting Health: {player.health}")
        print(f"  📦 Deck size: {len(player.deck)} cards\n")

    game = GameState([player1, player2])
    current_player = game.current_player()

    for p in [player1, player2]:
        draw_card(p, value=3)


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

            elif command.strip() == "use":
                ability_ref = player.main_character.active_ability_ref
                meta = CHARACTER_ABILITY_METADATA.get(ability_ref)
                func = CHARACTER_ABILITY_REGISTRY.get(ability_ref)

                if not ability_ref or not meta or not func:
                    print("❌ Your character has no active ability.")
                    continue

                if meta["type"] != "active":
                    print("❌ Your character has no *active* ability.")
                    continue

                cost = meta.get("cost", 0)
                if player.energy < cost:
                    print(f"🚫 Not enough energy to use {ability_ref} (costs {cost}, you have {player.energy})")
                    continue

                print("\n🧙 Active Abilities:")
                print("  0: Cancel")
                print(f"  1: {ability_ref} — {meta['description']} (Cost: {cost})")

                choice = input("Select ability: ").strip()
                if choice != "1":
                    print("↩️ Cancelled.")
                    continue

                if meta.get("needs_target"):
                    target = choose_target(player.opponent)
                    if not target:
                        continue
                    func(player, target)
                else:
                    func(player)

                player.energy -= cost
                print(f"🔥 Used {ability_ref} (Remaining energy: {player.energy})")

            else:
                print("❓ Unknown command.")

        current_player = game.current_player()

if __name__ == "__main__":
    run_game()
