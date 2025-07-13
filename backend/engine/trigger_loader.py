from backend.engine.trigger_observer import trigger_observer

def register_card_triggers(card, owner):
    card.owner = owner
    card._registered_effects = []

    for binding in card.effect_bindings.all():
        trigger_code = binding.trigger.script_reference
        effect_func = binding.effect.get_executable()
        value = binding.value

        print(f"\n🔧 Setting up trigger for {card.name}: {trigger_code}")

        def make_effect(effect_func, value, bound_card):
            def effect(**kwargs):
                if kwargs.get("card") == bound_card:
                    print(f"🟢 on_play triggered for {bound_card.name}")
                    if value is not None:
                        effect_func(bound_card, value)
                    else:
                        effect_func(bound_card)
            return effect

        if trigger_code == "on_play":
            effect = make_effect(effect_func, value, card)
            trigger_observer.subscribe("card_played", effect)
            card._registered_effects.append(("card_played", effect))

        elif trigger_code == "on_friendly_death":
            def make_death_effect(effect_func, value, bound_card, bound_owner, binding):
                def effect(**kwargs):
                    died_card = kwargs.get("died_card")
                    print(f"🧪 Checking death trigger for {bound_card.name}")
                    print(f"🔎 Died card: {died_card.name}, Owner: {died_card.owner.name}, Zone: {died_card.zone}")
                    print(f"🔎 Bound owner: {bound_owner.name}, Expected zone: {binding.trigger.zone}")

                    if died_card is None:
                        print("❌ No died_card.")
                        return

                    if died_card.owner != bound_owner:
                        print("❌ died_card.owner does not match bound_owner.")
                        return

                    expected_zone = getattr(binding.trigger, "zone", None)
                    if expected_zone:
                        if bound_card.zone != expected_zone:
                            print(f"❌ Triggering card is not in expected zone: expected '{expected_zone}', got '{bound_card.zone}'")
                            return
                        else:
                            print(f"✅ Triggering card is in the correct zone: '{expected_zone}'")


                    print(f"✅ Triggering effect for {bound_card.name}")
                    if value is not None:
                        effect_func(bound_card, value)
                    else:
                        effect_func(bound_card)

                return effect

            effect = make_death_effect(effect_func, value, card, owner, binding)
            trigger_observer.subscribe("card_died", effect)
            card._registered_effects.append(("card_died", effect))

    bindings = list(card.effect_bindings.all())
    if not bindings:
        print(f"⚠️ {card.name} has NO effect bindings (no triggers)")
    else:
        print(f"✅ {card.name} has {len(bindings)} binding(s):")
        for b in bindings:
            print(f"   🔗 Trigger: {b.trigger.script_reference} → Effect: {b.effect.name} | Value: {b.value} | Zone: {getattr(b.trigger, 'zone', 'N/A')}")


def unregister_card_triggers(card):
    if hasattr(card, "_registered_effects"):
        for event_name, effect in card._registered_effects:
            trigger_observer.unsubscribe(event_name, effect)
        card._registered_effects.clear()
