from backend.engine.trigger_exec import execute_trigger


def play_card(player, index):
    if index < 0 or index >= len(player.hand):
        print("🚫 Invalid card index.")
        return
    
    card = player.hand.pop(index)

    card.owner = player
    player.board.append(card)

    print(f"▶️ {player.name} plays {card.name}")
    execute_trigger(card, "on_play")
    player.cards_played_this_turn += 1


def attack(attacker, defender):
    total_attack = 0
    for card in attacker.board:
        if card.power > 0:
            total_attack += card.power

    print(f"⚔️ {attacker.name} attacks {defender.name} directly!")
    defender.health -= total_attack
    print(f"💥 {defender.name} takes {total_attack} damage! Health: {defender.health}")
    execute_trigger(None, "on_attack", attacker)



def end_turn(game_state):
    current = game_state.current_player()
    print(f"🔚 {current.name} ends their turn.")
    execute_trigger(None, "on_turn_end", current)
    game_state.turn_index = 1 - game_state.turn_index
