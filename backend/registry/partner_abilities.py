PARTNER_ABILITY_REGISTRY = {}
PARTNER_ABILITY_METADATA = {}

def register_partner_ability(ref, meta):
    def decorator(func):
        PARTNER_ABILITY_REGISTRY[ref] = func
        PARTNER_ABILITY_METADATA[ref] = meta
        return func
    return decorator

@register_partner_ability("draw_boost", {
    "type": "passive",
    "trigger": "on_turn_start", 
    "limit_per_turn": 1,
    "reset": "every_2_turns", 
    "description": "Draw an extra card each turn while this partner is present.",
})
def draw_boost(player):
    from backend.registry.effects import draw_card
    draw_card(player, 1)


'''

in reset, do things like "every_turn", "every_3_turns", etc. or None (if it is one-time use)

'''