
CONDITION_REGISTRY = {}

def owner_below_10_health(card):
    if not hasattr(card, "owner") or not card.owner:
        print(f"❌ owner_below_10: Card '{card.name}' has no owner!")
        return False

    print(f"🔍 owner_below_10: {card.name} owner's HP = {card.owner.health}")
    return card.owner.health < 10

def played_2_cards_this_turn(card):
    return getattr(card.owner, "cards_played_this_turn", 0) >= 2

CONDITION_REGISTRY["owner_below_10"] = owner_below_10_health
CONDITION_REGISTRY["played_2_this_turn"] = played_2_cards_this_turn
