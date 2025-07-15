from backend.registry._base import AbilityRegistry
from backend.registry.effects import draw_card

SOLO_ABILITIES = AbilityRegistry()

@SOLO_ABILITIES.register(
    "draw_on_start",
    type="passive",
    description="Draw 1 extra card at game start.",
    trigger="on_turn_start",
    condition="is_players_first_turn"
)
def bonus_draw_on_start(player):
    draw_card(player, 1)

@SOLO_ABILITIES.register(
    "extra_energy_turn1",
    type="passive",
    description="Gain +1 energy on your first turn.",
    trigger="on_turn_start",
    condition="is_players_first_turn"
)
def bonus_extra_energy_turn1(player):
    player.energy += 1
    print(f"⚡ {player.name} receives 1 extra energy from solo bonus.")
