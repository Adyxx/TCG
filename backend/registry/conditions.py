CONDITION_REGISTRY = {}

def register_condition(name):
    def decorator(func):
        CONDITION_REGISTRY[name] = func
        return func
    return decorator

def evaluate_condition(name, subject, param=None, ref=None):
    func = CONDITION_REGISTRY.get(name)
    if not func:
        raise ValueError(f"Unknown condition: {name}")
    return func(subject, param=param, ref=ref)

def get_player(subject):
    return subject.owner if hasattr(subject, "owner") else subject

@register_condition("is_players_first_turn")
def is_players_first_turn(subject, param=None, ref=None):
    if hasattr(subject, "owner"):
        subject = subject.owner
    return getattr(subject, "turn_count", -1) == 0

@register_condition("owner_below_10_health")
def owner_below_10_health(card, param=None, ref=None):
    print("OWNER HP:", card.owner.health, "  owner_below_10_health? : ", card.owner.health < 10)
    return hasattr(card, "owner") and card.owner.health < 10

@register_condition("played_2_this_turn")
def played_2_cards_this_turn(card, param=None, ref=None):
    return getattr(card.owner, "cards_played_this_turn", 0) >= 2

@register_condition("cooldown_ready")
def cooldown_ready(player, param=None, ref=None):
    return player.cooldowns.get(ref, 0) <= 0

@register_condition("has_not_triggered_this_turn")
def has_not_triggered_this_turn(subject, param=None, ref=None):
    if hasattr(subject, "turn_usage"):
        return subject.turn_usage.get(ref, 0) == 0
    elif hasattr(subject, "owner") and hasattr(subject.owner, "turn_usage"):
        return subject.owner.turn_usage.get(ref, 0) == 0
    else:
        return False

@register_condition("is_friendly_turn")
def is_friendly_turn(subject, param=None, ref=None):
    player = get_player(subject)
    return getattr(player, "turn_count", -1) == 0

