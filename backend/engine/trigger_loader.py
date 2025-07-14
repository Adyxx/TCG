from backend.engine.trigger_observer import trigger_observer
from backend.registry.triggers import TRIGGER_REGISTRY
from backend.registry.conditions import CONDITION_REGISTRY

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
            continue

        base_effect = builder(card=card, owner=owner, binding=binding)

        condition = binding.condition
        if condition:
            script_reference = condition.script_reference
            condition_func = CONDITION_REGISTRY.get(script_reference)
            if not condition_func:
                continue

            def wrapped_effect(*args, **kwargs):
                if condition_func(card):
                    base_effect(*args, **kwargs)
                else:
                    pass

            effect_to_register = wrapped_effect
        else:
            effect_to_register = base_effect

        trigger_observer.subscribe(event, effect_to_register)
        card._registered_effects.append((event, effect_to_register, trigger_code))

def unregister_card_triggers(card):
    if hasattr(card, "_registered_effects"):
        for event_name, effect in card._registered_effects:
            trigger_observer.unsubscribe(event_name, effect)
        card._registered_effects.clear()

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

