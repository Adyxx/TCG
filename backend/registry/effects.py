
def apply_haste(card):
    print(f"{card.name} gains Haste!")

def draw_card(card):
    print(f"Drawing a card because of {card.name}'s ability.")

def self_hurt_2(card):
    player = card.owner
    player.health -= 2
    print(f"Dealing 2 points of damage to your hero because of {card.name}'s ability! Health is now {player.health}")

def override_deck_limit(card, new_limit):
    card.override_limit = new_limit

EFFECT_REGISTRY = {
    "apply_haste": apply_haste,
    "draw_card": draw_card,
    "self_hurt_2": self_hurt_2,
    "override_deck_limit": override_deck_limit,
}

'''

buff_strength

heal_3

'''