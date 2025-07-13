from backend.engine.trigger_observer import trigger_observer
from backend.registry.triggers import TRIGGER_REGISTRY
from backend.registry.conditions import CONDITION_REGISTRY

def register_card_triggers(card, owner):
    card.owner = owner
    card._registered_effects = []

    bindings = list(card.effect_bindings.all())
    if not bindings:
        print(f"⚠️ {card.name} has NO effect bindings (no triggers)")
        return

    print(f"\n🔧 Setting up {len(bindings)} trigger(s) for {card.name}")

    for binding in bindings:
        trigger_code = binding.trigger.script_reference
        trigger_meta = TRIGGER_REGISTRY.get(trigger_code)

        if not trigger_meta:
            print(f"❌ Unknown trigger: {trigger_code}")
            continue

        builder = trigger_meta.get("builder")
        event = trigger_meta.get("event")

        if not event or not builder:
            print(f"⏭️ Skipping trigger '{trigger_code}' – not runtime-registerable")
            continue

        base_effect = builder(card=card, owner=owner, binding=binding)

        # === Wrap with condition if one exists ===
        condition = binding.condition
        if condition:
            print(condition.script_reference)
            condition_func = CONDITION_REGISTRY.get(condition.script_reference)
            print(condition_func)
            if not condition_func:
                print(f"❌ Unknown condition '{condition.script_reference}' for {card.name}")
                continue

            def wrapped_effect(*args, **kwargs):
                if condition_func(card):
                    base_effect(*args, **kwargs)
                else:
                    print(f"🚫 Condition '{condition.script_reference}' failed for {card.name}, skipping effect.")

            effect_to_register = wrapped_effect
            print(f"🔗 {card.name}: Effect will run only if condition '{condition.script_reference}' passes.")
        else:
            effect_to_register = base_effect

        trigger_observer.subscribe(event, effect_to_register)
        card._registered_effects.append((event, effect_to_register))

        print(f"✅ {card.name} registered '{trigger_code}' to '{event}'")

def unregister_card_triggers(card):
    if hasattr(card, "_registered_effects"):
        for event_name, effect in card._registered_effects:
            trigger_observer.unsubscribe(event_name, effect)
        card._registered_effects.clear()
