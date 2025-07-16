from backend.engine.trigger_observer import trigger_observer
from backend.engine.trigger_loader import unregister_card_trigger
from enum import Enum

class DamageType(Enum):
    COMBAT = "combat"
    ABILITY = "ability"
    SPELL = "spell"
    OTHER = "other"

def get_targets(player, target_spec):
    if target_spec == "enemy:board":
        return player.opponent.board
    elif target_spec == "enemy:hero":
        return [player.opponent]
    elif target_spec == "enemy:board_or_hero":
        return player.opponent.board + [player.opponent]
    elif target_spec == "friendly:board":
        return player.board
    elif target_spec == "self":
        return [player]
    elif callable(target_spec):
        return target_spec(player)
    else:
        return []

def choose_target(player, target_spec):
    targets = get_targets(player, target_spec)
    if not targets:
        print("❌ No valid targets.")
        return None

    print("\n🎯 Choose target:")
    for i, target in enumerate(targets):
        if hasattr(target, "power"):
            desc = f"{target.name} (Power: {target.power}, Health: {target.health - target.damage_taken})"
        else:
            desc = f"{target.name} (HP: {target.health})"
        print(f"  {i}: {desc}")

    try:
        idx = int(input("Choose target ID: "))
        return targets[idx]
    except (ValueError, IndexError):
        print("❌ Invalid selection.")
        return None

def resolve_damage(source, target, amount, damage_type=DamageType.OTHER):
    print(f"💥 {source.name} deals {amount} damage to {target.name} ({damage_type.name})")

    if hasattr(target, "damage_taken"): 
        target.damage_taken += amount
        if target.damage_taken >= target.health:
            owner = target.owner
            if owner:
                unregister_card_trigger(target, "on_friendly_death") 
                owner.board.remove(target)
                owner.graveyard.append(target)
            print(f"💀 {target.name} is destroyed!")
            trigger_observer.emit("card_died", died_card=target, owner=owner)
    else:
        target.health -= amount
        if target.health <= 0:
            print(f"☠️ {target.name} has died!")
            trigger_observer.emit("player_died", player=target)

def resolve_heal(source, target, amount):
    print(f"💚 {source.name} heals {target.name} for {amount} HP.")
    target.health += amount
    trigger_observer.emit("healed", source=source, target=target, amount=amount)

def resolve_combat(attacker_card, target, attacker, defender):
    print(f"⚔️ {attacker_card.name} attacks {target.name}!")
    trigger_observer.emit("card_attacked", card=attacker_card, target=target)

    resolve_damage(attacker_card, target, attacker_card.power, damage_type=DamageType.COMBAT)

    if hasattr(target, "power"):
        resolve_damage(target, attacker_card, target.power, damage_type=DamageType.COMBAT)

    attacker_card.tapped = True

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

    print("\n🎯 Choose target type:")
    print("  0: Enemy hero")
    print("  1: Enemy card")

    choice = input("Target type: ").strip()

    if choice == "0":
        target_spec = "enemy:hero"
    elif choice == "1":
        target_spec = "enemy:board"
    else:
        print("❌ Invalid choice.")
        return

    target = choose_target(attacker, target_spec)
    if not target:
        return

    resolve_combat(attacker_card, target, attacker, defender)

def use_ability(player, opponent):
    from backend.registry.character_abilities import CHARACTER_ABILITIES

    ability_ref = player.main_character.active_ability_ref
    meta = CHARACTER_ABILITIES.get_metadata(ability_ref)
    func = CHARACTER_ABILITIES.get_function(ability_ref)

    if not ability_ref or not meta or not func:
        print("❌ No active ability.")
        return
    if meta["type"] != "active":
        print("❌ Not an active ability.")
        return

    cost = meta.get("cost", 0)
    if player.energy < cost:
        print(f"🚫 Not enough energy ({cost} needed, you have {player.energy})")
        return

    print("\n🧙 Active Abilities:")
    print("  0: Cancel")
    print(f"  1: {ability_ref} — {meta['description']} (Cost: {cost})")
    choice = input("Select ability: ").strip()
    if choice != "1":
        print("↩️ Cancelled.")
        return

    if meta.get("needs_target"):
        target_spec = meta.get("target_spec", "enemy:hero")
        target = choose_target(player, target_spec)
        if not target:
            return
        func(player, target)
    else:
        func(player)

    player.energy -= cost
    print(f"🔥 Used {ability_ref} (Remaining energy: {player.energy})")


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

    if card.card_type == "SPELL":
        print(f"✨ {player.name} casts spell: {card.name}")
        card.zone = "graveyard"
        player.graveyard.append(card)

    else:
        card.zone = "board"
        player.board.append(card)
        print(f"▶️ {player.name} plays {card.name} to the board")

        bindings = card.effect_bindings.all()
        for binding in bindings:
            print("🧩 [Binding Debug Info]")
            print(f"   → Trigger: {binding.trigger.script_reference}")
            print(f"   → Effect: {binding.effect.name} (Requires Target: {binding.effect.requires_target}, Value: {binding.value})")
            print(f"   → Target Spec: {binding.target_spec}")
            print(f"   → Condition: {binding.condition}")
            print(f"   → Restriction: {binding.restriction}")


    player.energy -= cost
    print(f"▶️ {player.name} plays {card.name} for {cost} energy (Remaining: {player.energy})")

    trigger_observer.emit("card_played", card=card, owner=player)
    player.cards_played_this_turn += 1

def start_turn(player):
    player.start_turn()

def end_turn(player):
    player.end_turn()
