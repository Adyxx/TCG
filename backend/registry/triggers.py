import importlib

TRIGGER_REGISTRY = {
    "on_play": {
        "description": "Triggered when the card is played from hand",
        "event": "card_played",
        "builder": None,
    },
    "on_death": {
        "description": "Triggered when this card dies",
        "event": "card_died",
        "builder": None,
    },
    "on_friendly_death": {
        "description": "Triggered when a friendly card dies",
        "event": "card_died",
        "builder": None,
    },
    "on_turn_start": {
        "description": "Triggered at the beginning of a player's turn",
        "event": "turn_started",
        "builder": None,
    },
    "on_turn_end": {
        "description": "Triggered at the end of a player's turn",
        "event": "turn_ended",
        "builder": None,
    },
    "on_attack": {
        "description": "Triggered when this card attacks",
        "event": "card_attacked",
        "builder": None,
    },
    "on_deck_build": {
        "description": "Used only for deck-building validation",
        "event": None,
        "builder": None,
    },
}


for trigger_code in TRIGGER_REGISTRY:
    try:
        module = importlib.import_module(f"backend.engine.triggers.{trigger_code}")
        TRIGGER_REGISTRY[trigger_code]["builder"] = module.build
    except ModuleNotFoundError:
        print(f"⚠️ Trigger module '{trigger_code}' not found in backend.engine.triggers")
    except AttributeError:
        print(f"⚠️ Module '{trigger_code}' does not define a `build()` function")
