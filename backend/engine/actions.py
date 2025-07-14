from backend.engine.trigger_observer import trigger_observer
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


def choose_target(defender):
    print("\n🎯 Choose target:")
    print(f"  0: {defender.name} directly (HP: {defender.health})")
    for i, card in enumerate(defender.board):
        print(f"  {i + 1}: {card.name} (Power: {card.power}, Health: {card.health - card.damage_taken})")

    try:
        target_idx = int(input("Choose target ID: "))
    except ValueError:
        print("❌ Invalid input.")
        return None

    if target_idx == 0:
        return defender
    elif 1 <= target_idx <= len(defender.board):
        return defender.board[target_idx - 1]
    else:
        print("❌ Invalid target.")
        return None


def resolve_combat(attacker_card, target, attacker, defender):
    if isinstance(target, type(defender)):
        print(f"💥 {attacker_card.name} attacks {defender.name} for {attacker_card.power} damage!")
        trigger_observer.emit("card_attacked", card=attacker_card, target=defender)
        defender.health -= attacker_card.power
        attacker_card.tapped = True
        print(f"❤️ {defender.name} now has {defender.health} HP.")
        return

    print(f"⚔️ {attacker_card.name} attacks {target.name}!")
    trigger_observer.emit("card_attacked", card=attacker_card, target=target)

    target.damage_taken += attacker_card.power
    attacker_card.damage_taken += target.power

    death_queue = []

    if target.damage_taken >= target.health:
        defender.board.remove(target)
        defender.graveyard.append(target)
        death_queue.append(target)
        print(f"💀 {target.name} is destroyed!")

    if attacker_card.damage_taken >= attacker_card.health:
        attacker.board.remove(attacker_card)
        attacker.graveyard.append(attacker_card)
        death_queue.append(attacker_card)
        print(f"💀 {attacker_card.name} is destroyed!")
    else:
        attacker_card.tapped = True

    for dead_card in death_queue:
        trigger_observer.emit("card_died", died_card=dead_card, owner=dead_card.owner)


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

    target = choose_target(defender)
    if not target:
        return

    resolve_combat(attacker_card, target, attacker, defender)


def use_ability(player, opponent):
    from backend.registry.character_abilities import CHARACTER_ABILITY_METADATA, CHARACTER_ABILITY_REGISTRY

    ability_ref = player.main_character.active_ability_ref
    meta = CHARACTER_ABILITY_METADATA.get(ability_ref)
    func = CHARACTER_ABILITY_REGISTRY.get(ability_ref)

    if not ability_ref or not meta or not func:
        print("❌ Your character has no active ability.")
        return

    if meta["type"] != "active":
        print("❌ Your character has no *active* ability.")
        return

    cost = meta.get("cost", 0)
    if player.energy < cost:
        print(f"🚫 Not enough energy to use {ability_ref} (costs {cost}, you have {player.energy})")
        return

    print("\n🧙 Active Abilities:")
    print("  0: Cancel")
    print(f"  1: {ability_ref} — {meta['description']} (Cost: {cost})")

    choice = input("Select ability: ").strip()
    if choice != "1":
        print("↩️ Cancelled.")
        return

    if meta.get("needs_target"):
        target = choose_target(opponent)
        if not target:
            return
        func(player, target)
    else:
        func(player)

    player.energy -= cost
    print(f"🔥 Used {ability_ref} (Remaining energy: {player.energy})")



def start_turn(player):
    print(f"▶️ {player.name}'s turn begins.")
    player.energy += 1
    print(f"⚡ {player.name} gains 1 energy → {player.energy} total")

    draw_card(player, value=1)

    player._class_trait_uses_this_turn = 0
    player._passive_uses_this_turn = 0

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
