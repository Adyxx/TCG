ENERGY_SYSTEM = {
    "KNIGHT": {
        "description": "Gain +1 temporary energy when a friendly unit dies (max once per turn).",
        "trigger": "on_friendly_death",
        "limit_per_turn": 1,
    },
    "WIZARD": {
        "description": "Discard a card to gain +1 temporary energy.",
        "trigger": "on_card_discard",
        "limit_per_turn": 2,
    },
    # etc.
}
