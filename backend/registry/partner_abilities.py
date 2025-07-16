from backend.registry._base import AbilityRegistry
from backend.registry.effects import draw_card

PARTNER_ABILITIES = AbilityRegistry()

@PARTNER_ABILITIES.register(
    "draw_boost",
    type="passive",
    trigger="on_turn_start",
    cooldown=2,
    condition="cooldown_ready",
    description="Draw an extra card every 2 turns while this partner is present."
)

def draw_boost(player):
    draw_card(source=None, target=player, value=1)
