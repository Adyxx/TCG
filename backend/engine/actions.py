
from backend.engine.trigger_observer import trigger_observer
from backend.engine.trigger_loader import unregister_card_triggers
from backend.registry.effects import draw_card

def play_card(player, index):
    if index < 0 or index >= len(player.hand):
        print("🚫 Invalid card index.")
        return
    
    card = player.hand[index]
    cost = card.cost

    if player.energy < cost:
        print(f"🚫 Not enough energy! Needed {cost}, but you have {player.energy}.")
        return

    player.hand.pop(index)
    card.owner = player
    card.zone = "board"
    player.board.append(card)
    player.energy -= cost

    print(f"▶️ {player.name} plays {card.name} for {cost} energy (Remaining: {player.energy})")

    trigger_observer.emit("card_played", card=card, owner=player)
    player.cards_played_this_turn += 1



def attack(attacker, defender):
    attackers = [card for card in attacker.board if not card.summoning_sickness and not card.tapped and card.power > 0]
    if not attackers:
        print(f"{attacker.name} has no available attackers.")
        return

    print("\n⚔️ Available attackers:")
    for i, card in enumerate(attackers):
        print(f"  {i}: {card.name} (Power: {card.power}, Health: {card.health - card.damage_taken})")

    try:
        attacker_idx = int(input("Choose attacker ID: "))
        attacker_card = attackers[attacker_idx]
    except (ValueError, IndexError):
        print("❌ Invalid attacker choice.")
        return

    print("\n🎯 Choose target:")
    print(f"  0: Attack {defender.name} directly (HP: {defender.health})")
    for i, card in enumerate(defender.board):
        print(f"  {i+1}: {card.name} (Power: {card.power}, Health: {card.health - card.damage_taken})")

    try:
        target_idx = int(input("Choose target ID: "))
    except ValueError:
        print("❌ Invalid input.")
        return
    

    if target_idx == 0:
        print(f"💥 {attacker_card.name} attacks {defender.name} for {attacker_card.power} damage!")

        trigger_observer.emit("card_attacked", card=attacker_card, target=defender)
        #trigger_observer.emit("on_attacked", card=defender, attacker=attacker_card)

        defender.health -= attacker_card.power
        attacker_card.tapped = True
        print(f"❤️ {defender.name} now has {defender.health} HP.")
        return

    elif 1 <= target_idx <= len(defender.board):
        target_card = defender.board[target_idx - 1]
        print(f"⚔️ {attacker_card.name} attacks {target_card.name}!")

        print(f"📤 Emitting 'on_attack' for card object {id(attacker_card)}: {attacker_card.name}")

        trigger_observer.emit("card_attacked", card=attacker_card, target=target_card)
        #trigger_observer.emit("on_attacked", card=target_card, attacker=attacker_card)

        target_card.damage_taken += attacker_card.power
        attacker_card.damage_taken += target_card.power

        death_queue = []

        if target_card.damage_taken >= target_card.health:
            defender.board.remove(target_card)
            defender.graveyard.append(target_card)
            death_queue.append(target_card)
            print(f"💀 {target_card.name} is destroyed!")

        if attacker_card.damage_taken >= attacker_card.health:
            attacker.board.remove(attacker_card)
            attacker.graveyard.append(attacker_card)
            death_queue.append(attacker_card)
            print(f"💀 {attacker_card.name} is destroyed!")
        else:
            attacker_card.tapped = True

        for dead_card in death_queue:
            unregister_card_triggers(dead_card)
            trigger_observer.emit("card_died", died_card=dead_card, owner=dead_card.owner)


    else:
        print("❌ Invalid target.")
        return


def start_turn(player):
    print(f"▶️ {player.name}'s turn begins.")

    player.energy += 1
    player._class_trait_uses_this_turn = 0
    print(f"⚡ {player.name} gains 1 energy → {player.energy} total")

    draw_card(player, value=1)

    trigger_observer.emit("turn_started", player=player)
    for card in player.board:
        trigger_observer.emit("turn_started", card=card, player=player)

    for card in player.board:
        card.tapped = False
        card.summoning_sickness = False

def end_turn(player):
    print(f"⏹ {player.name}'s turn ends.")
    trigger_observer.emit("turn_ended", player=player)
    for card in player.board:
        trigger_observer.emit("turn_ended", card=card, player=player)
