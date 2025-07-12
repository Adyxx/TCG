CHARACTER_ABILITY_REGISTRY = {}
CHARACTER_ABILITY_METADATA = {}

def register_ability(name, *, type, description, cost=None, trigger=None, limit=None):
    def wrapper(func):
        CHARACTER_ABILITY_REGISTRY[name] = func
        CHARACTER_ABILITY_METADATA[name] = {
            "type": type,
            "description": description,
            "cost": cost,
            "trigger": trigger,
            "limit_per_turn": limit,
        }
        return func
    return wrapper

@register_ability("fireball", type="active", description="Deal 3 damage to a target.", cost=2)
def fireball(player, target):
    target.take_damage(3)

@register_ability("healing_aura", type="passive", description="Heal 1 at start of turn", trigger="on_turn_start")
def healing_aura(player):
    player.heal(1)
