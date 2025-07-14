DECK_RESTRICTION_REGISTRY = {}

def register_restriction(name):
    def wrapper(func):
        DECK_RESTRICTION_REGISTRY[name] = func
        return func
    return wrapper

@register_restriction("charlotte_4_cost_or_less")
def charlotte_4_cost_or_less(deck):
    for dc in deck.deck_cards.select_related("card"):
        if dc.card.cost > 4:
            return False, "Charlotte can only include cards that cost 4 or less."
    return True, None

@register_restriction("paul_10_pirates")
def paul_needs_10_pirates(deck):
    pirate_count = 0
    for dc in deck.deck_cards.select_related("card"):
        if "Pirate" in [s.name for s in dc.card.subtypes.all()]:
            pirate_count += dc.quantity
    if pirate_count < 10:
        return False, "Paul's deck must include at least 10 Pirate cards."
    return True, None
