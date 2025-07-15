SOLO_BONUS_REGISTRY = {}
SOLO_BONUS_METADATA = {}

def register_solo_bonus(ref, meta):
    def decorator(func):
        SOLO_BONUS_REGISTRY[ref] = func
        SOLO_BONUS_METADATA[ref] = meta
        return func
    return decorator


@register_solo_bonus("draw_on_start", {
    "description": "Draw 1 extra card at game start.",
    "timing": "game_start"
})
def bonus_draw_on_start(player):
    from backend.registry.effects import draw_card
    draw_card(player, 1)


@register_solo_bonus("extra_energy_turn1", {
    "description": "Gain +1 energy on your first turn.",
    "timing": "start_of_first_turn"
})
def bonus_extra_energy_turn1(player):
    player.energy += 1
    print(f"⚡ {player.name} receives 1 extra energy from solo bonus.")
