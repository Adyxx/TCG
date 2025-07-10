
def apply_haste(card):
    print(f"{card.name} gains Haste!")

def draw_card(card):
    print(f"Drawing a card because of {card.name}'s ability.")

def self_hurt_2(card):
    print(f"Dealing 2 points of damage to your hero because of {card.name}'s ability.")

EFFECT_REGISTRY = {
    "haste": apply_haste,
    "draw_card": draw_card,
    "self_hurt_2": self_hurt_2,
}

'''

buff_strength

heal_3

'''