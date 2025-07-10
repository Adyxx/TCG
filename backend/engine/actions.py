from backend.engine.trigger_exec import execute_trigger


def play_card(player, index):
    if index < 0 or index >= len(player.hand):
        print("🚫 Invalid card index.")
        return

    card = player.hand.pop(index)
    print(f"▶️ {player.name} plays {card.name}")
    execute_trigger(card, "on_play")
    player.cards_played_this_turn += 1


def attack(player, target_player):
    print(f"⚔️ {player.name} attacks {target_player.name} directly!")
    target_player.health -= 2
    print(f"💥 {target_player.name} takes 2 damage! Health: {target_player.health}")
    if target_player.health <= 0:
        print(f"🏁 {target_player.name} has been defeated!")
        player.game_state.game_over = True


def end_turn(game_state):
    current = game_state.current_player()
    print(f"🔚 {current.name} ends their turn.")
    execute_trigger(None, "on_turn_end", current)
    game_state.turn_index = 1 - game_state.turn_index
