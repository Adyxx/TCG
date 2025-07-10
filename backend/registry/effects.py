
def apply_haste(card):
    print(f"{card.name} gains Haste!")

def draw_card(card):
    print(f"Drawing a card because of {card.name}'s ability.")

EFFECT_REGISTRY = {
    "haste": apply_haste,
    "draw_card": draw_card,
}
