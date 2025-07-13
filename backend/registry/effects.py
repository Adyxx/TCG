


def apply_haste(card):
    print(f"{card.name} gains Haste!")

def draw_card(player, value=1):
    for _ in range(value):
        if player.deck:
            drawn = player.deck.pop(0)
            drawn.owner = player
            player.hand.append(drawn)
            print(f"🃏 {player.name} drew {drawn.name}.")
        else:
            print(f"⚠️ {player.name}'s deck is empty!")

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
    "apply_haste": {
        "func": apply_haste,
        "target": "card",
    },
    "draw_card": {
        "func": draw_card,
        "target": "player",
    },
    "self_hurt": {
        "func": self_hurt,
        "target": "card",
    },
    "override_deck_limit": {
        "func": override_deck_limit,
        "target": "card",
    },
}
 