def build(card, owner, binding):
    effect_func, target = binding.effect.get_executable() 
    value = binding.value
    expected_zone = getattr(binding.trigger, "zone", None)

    def effect(**kwargs):
        died_card = kwargs.get("died_card")
        if died_card is None:
            #print(f"❌ [on_friendly_death] No died_card provided.")
            return

        #print(f"🧪 [on_friendly_death] Checking for {card.name}")
        #print(f"   🪦 Died: {died_card.name} | Owner: {died_card.owner.name} | Zone: {died_card.zone}")
        #print(f"   🎯 Expected owner: {owner.name}, Zone: {expected_zone or 'ANY'}")

        if died_card.owner != owner:
            #print(f"❌ Not a friendly death.")
            return

        if expected_zone and card.zone != expected_zone:
            #print(f"❌ {card.name} not in expected zone: {expected_zone} (is in {card.zone})")
            return

        #print(f"✅ [on_friendly_death] Triggering effect for {card.name}")

        target_obj = {
            "card": card,
            "player": owner,
        }[target]

        if value is not None:
            effect_func(target_obj, value)
        else:
            effect_func(target_obj)

    return effect
