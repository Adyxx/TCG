from backend.registry._base import AbilityRegistry
from backend.engine.actions import resolve_damage, resolve_heal, DamageType

CHARACTER_ABILITIES = AbilityRegistry()

@CHARACTER_ABILITIES.register(
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

@CHARACTER_ABILITIES.register(
    "healing_aura",
    type="passive",
    description="Heal 1 at start of turn.",
    trigger="on_turn_start",
    condition="has_not_triggered_this_turn",
    effect_type={"heal": "self"},
    target_spec="self"
)
def healing_aura(player):
    resolve_heal(source=player, target=player, amount=1)
