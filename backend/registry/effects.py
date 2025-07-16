from backend.engine.actions import resolve_damage, DamageType 

def apply_haste(source, target, value=None):
    print(f"{target.name} gains Haste! (via {source.name})")

def draw_card(source, target, value):
    player = target
    for _ in range(int(value)):
        if player.deck:
            drawn = player.deck.pop(0)
            drawn.owner = player
            player.hand.append(drawn)
            print(f"🃏 {player.name} drew {drawn.name}")
        else:
            print(f"⚠️ {player.name}'s deck is empty!")

def override_deck_limit(source, target, value):
    target.override_limit = value

def deal_damage(source, target, value):
    print(f"[🧪] deal_damage(): source={getattr(source, 'name', 'Unknown')}, target={target.name}, value={value}")
    resolve_damage(source=source, target=target, amount=value, damage_type=DamageType.OTHER)



EFFECT_REGISTRY = {
    "apply_haste": {
        "func": apply_haste,
        "target": "card",
    },
    "draw_card": {
        "func": draw_card,
        "target": "player",
    },
    "override_deck_limit": {
        "func": override_deck_limit,
        "target": "card",
    },
    "deal_damage": {
        "func": deal_damage,
        "target": None, 
    },
}
 