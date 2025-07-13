def apply_haste(card):
    print(f"{card.name} gains Haste!")

def draw_card(card, value=1):
    try:
        amount = int(value)
    except (ValueError, TypeError):
        amount = 1
    print(f"Drawing {amount} card(s) because of {card.name}'s ability.")

def self_hurt(card, damage):
    player = card.owner
    if player is None:
        print(f"❌ Cannot self-hurt: card.owner is None for {card.name}")
        return
    player.health -= damage
    print(f"Dealing {damage} points of damage to your hero because of {card.name}'s ability! Health is now {player.health}")

def override_deck_limit(card, new_limit):
    card.override_limit = new_limit

EFFECT_REGISTRY = {
    "apply_haste": apply_haste,
    "draw_card": draw_card,
    "self_hurt": self_hurt,
    "override_deck_limit": override_deck_limit,
}
