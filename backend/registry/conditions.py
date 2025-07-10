
CONDITION_REGISTRY = {}

def owner_below_10_health(card):
    return getattr(card.owner, "health", 999) < 10

def played_2_cards_this_turn(card):
    return getattr(card.owner, "cards_played_this_turn", 0) >= 2

CONDITION_REGISTRY["owner_below_10"] = owner_below_10_health
CONDITION_REGISTRY["played_2_this_turn"] = played_2_cards_this_turn
