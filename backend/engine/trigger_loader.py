from backend.engine.trigger_observer import trigger_observer
from backend.registry.triggers import TRIGGER_REGISTRY

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

        effect = builder(card=card, owner=owner, binding=binding)
        trigger_observer.subscribe(event, effect)
        card._registered_effects.append((event, effect))

        print(f"✅ {card.name} registered '{trigger_code}' to '{event}'")

def unregister_card_triggers(card):
    if hasattr(card, "_registered_effects"):
        for event_name, effect in card._registered_effects:
            trigger_observer.unsubscribe(event_name, effect)
        card._registered_effects.clear()
