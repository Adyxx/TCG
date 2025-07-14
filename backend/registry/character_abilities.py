from backend.engine.actions import resolve_damage, resolve_heal, DamageType

CHARACTER_ABILITY_REGISTRY = {}
CHARACTER_ABILITY_METADATA = {}

def register_ability(name, *, type, description, cost=None, trigger=None, limit=None, needs_target=False, effect_type=None, target_spec=None):
    def wrapper(func):
        CHARACTER_ABILITY_REGISTRY[name] = func
        CHARACTER_ABILITY_METADATA[name] = {
            "type": type,
            "description": description,
            "cost": cost,
            "trigger": trigger,
            "limit_per_turn": limit,
            "needs_target": needs_target,
            "effect_type": effect_type,
            "target_spec": target_spec,
        }
        return func
    return wrapper


@register_ability(
    "fireball",
    type="active",
    description="Deal 3 damage to a target.",
    cost=2,
    needs_target=True,
    effect_type={"damage": "single"},
    target_spec="enemy:board_or_hero"
)
def fireball(player, target):
    resolve_damage(source=player, target=target, amount=3, damage_type=DamageType.ABILITY)


@register_ability(
    "healing_aura",
    type="passive",
    description="Heal 1 at start of turn",
    limit=1,
    trigger="on_turn_start",
    effect_type={"heal": "self"},
    target_spec="self"
)
def healing_aura(player):
    resolve_heal(source=player, target=player, amount=1)
