from backend.engine.trigger_observer import trigger_observer

from backend.registry.triggers import TRIGGER_REGISTRY
from backend.registry.conditions import CONDITION_REGISTRY, evaluate_condition

def get_ability_sources():
    from backend.registry.character_abilities import CHARACTER_ABILITIES
    from backend.registry.partner_abilities import PARTNER_ABILITIES
    from backend.registry.solo_abilities import SOLO_ABILITIES
    from backend.registry.class_traits import CLASS_TRAITS

    return {
        "character": CHARACTER_ABILITIES,
        "partner": PARTNER_ABILITIES,
        "solo": SOLO_ABILITIES,
        "class": CLASS_TRAITS,
    }

def register_card_triggers(card, owner):
    card.owner = owner
    card._registered_effects = []

    bindings = list(card.effect_bindings.all())
    if not bindings:
        return

    for binding in bindings:
        trigger_code = binding.trigger.script_reference
        trigger_meta = TRIGGER_REGISTRY.get(trigger_code)

        if not trigger_meta:
            continue

        builder = trigger_meta.get("builder")
        event = trigger_meta.get("event")

        if not event or not builder:
            #print(f"⚠️ Skipping binding: missing event or builder for trigger '{trigger_code}' on {card.name}")
            continue

        base_effect = builder(card=card, owner=owner, binding=binding)

        if not callable(base_effect):
            print(f"❌ Builder for trigger '{trigger_code}' did not return a valid effect for {card.name}")
            continue


        condition = binding.condition
        if condition:
            condition_name = condition.script_reference
            condition_func = CONDITION_REGISTRY.get(condition_name)

            if not condition_func:
                print(f"❌ Unknown condition '{condition_name}' for {card.name}")
                continue

            def make_wrapped_effect(card, binding, base_effect, condition_name):
                def wrapped_effect(*args, **kwargs):
                    if evaluate_condition(condition_name, card, param=binding.value, ref=binding.effect.name):
                        base_effect(**kwargs)

                return wrapped_effect

            effect_to_register = make_wrapped_effect(card, binding, base_effect, condition_name)
        else:
            effect_to_register = base_effect


        print(effect_to_register)
        trigger_observer.subscribe(event, effect_to_register)
        #card._registered_effects.append((event, effect_to_register))
        card._registered_effects.append((event, effect_to_register, trigger_code))
        

def unregister_card_trigger(card, trigger_code_to_remove):
    if not hasattr(card, "_registered_effects"):
        return

    to_keep = []
    for event_name, effect, trigger_code in card._registered_effects:
        if trigger_code == trigger_code_to_remove:
            trigger_observer.unsubscribe(event_name, effect)
        else:
            to_keep.append((event_name, effect, trigger_code))

    card._registered_effects = to_keep


def register_player_ability(player, ability_type: str, ref: str):
    registry = get_ability_sources()[ability_type]
    meta = registry.get_metadata(ref)
    func = registry.get_function(ref)

    if not meta or not func:
        print(f"⚠️ {ability_type} ability '{ref}' is invalid or missing.")
        return

    attr_prefix = {
        "solo": "solo_bonus",
        "partner": "partner_ability",
        "character": "passive_ability",
        "class": "class_trait",
    }[ability_type]

    if meta["type"] == "passive":
        result = registry.build_wrapped_passive(player, ref, attr_prefix)
        if not result:
            return

        trigger_code, wrapped = result
        trigger_meta = TRIGGER_REGISTRY.get(trigger_code)
        print(trigger_meta)
        if not trigger_meta or not trigger_meta.get("event"):
            print(f"❌ Missing event for passive trigger: {ref}")
            return

        trigger_observer.subscribe(trigger_meta["event"], wrapped)
        setattr(player, attr_prefix, meta)

        print(f"✅ Registered passive {ability_type} '{ref}' for {player.name}")

    elif meta["type"] == "active":
        setattr(player, attr_prefix, {
            "name": ref,
            "description": meta.get("description", ""),
            "function": func,
            "cooldown": meta.get("cooldown", 0),
            "cost": meta.get("cost", 0),
            "targeted": meta.get("targeted", False),
        })

        if not hasattr(player, "cooldowns"):
            player.cooldowns = {}
        player.cooldowns[ref] = 0  
        
        print(f"🎯 Registered active {ability_type} '{ref}' for {player.name}")

    else:
        setattr(player, attr_prefix, {
            "name": ref,
            "description": meta.get("description", ""),
            "function": func,
            "timing": meta.get("timing", "game_start")
        })
        print(f"🎁 Registered {ability_type} '{ref}' for {player.name}")

def reset_player_abilities(player):
    player.turn_usage = {}