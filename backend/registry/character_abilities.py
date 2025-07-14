CHARACTER_ABILITY_REGISTRY = {}
CHARACTER_ABILITY_METADATA = {}

def register_ability(name, *, type, description, cost=None, trigger=None, limit=None, needs_target=False):
    def wrapper(func):
        CHARACTER_ABILITY_REGISTRY[name] = func
        CHARACTER_ABILITY_METADATA[name] = {
            "type": type,
            "description": description,
            "cost": cost,
            "trigger": trigger,
            "limit_per_turn": limit,
            "needs_target": needs_target,
        }
        return func
    return wrapper

@register_ability("fireball", type="active", description="Deal 3 damage to a target.", cost=2, needs_target=True)
def fireball(player, target):
    print(f"💥 {player.name} casts Fireball on {target.name}!")
    target.health -= 3
    print(f"🩸 {target.name} now has {target.health} HP.")

@register_ability("healing_aura", type="passive", description="Heal 1 at start of turn", trigger="on_turn_start")
def healing_aura(player):
    print(f"💚 {player.name} heals for 1 HP.")
    player.health += 1
