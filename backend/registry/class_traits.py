CLASS_TRAITS = {
    "KNIGHT": {
        "description": "Gain +1 temporary energy when a unit dies (max once per turn).",
        "trigger": "on_friendly_death",
        "limit_per_turn": 1,
        "effect": lambda player: setattr(player, "energy", player.energy + 1) 
    },
    "WIZARD": {
        "description": "Discard a card to gain +1 temporary energy.",
        "trigger": "on_discard",
        "limit_per_turn": 2,
        "effect": lambda player: setattr(player, "energy", player.energy + 1)
    },
}
