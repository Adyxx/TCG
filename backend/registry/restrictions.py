
RESTRICTION_REGISTRY = {}

def max_3_per_turn(card, binding_id):
    key = f"{card.id}_{binding_id}_trigger_count"
    count = RESTRICTION_STATE.get(key, 0)

    if count >= 3:
        return False

    RESTRICTION_STATE[key] = count + 1
    return True

RESTRICTION_STATE = {}

def reset_restriction_state():
    global RESTRICTION_STATE
    RESTRICTION_STATE = {}

RESTRICTION_REGISTRY["max_3_per_turn"] = max_3_per_turn
