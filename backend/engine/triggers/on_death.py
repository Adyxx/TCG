
def build(card, owner, binding):
    effect_func, target = binding.effect.get_executable()
    value = binding.value

    def effect(**kwargs):
        died_card = kwargs.get("died_card")
        if died_card is None:
            #print(f"❌ [on_death] No died_card provided.")
            return

        #print(f"🧪 [on_death] Checking death match for {card.name} vs {died_card.name}")
        if died_card != card:
            #print(f"❌ [on_death] {card.name} did not die — skipping.")
            return

        #print(f"✅ [on_death] Triggering effect for {card.name}")

        target_obj = {
            "card": card,
            "player": owner,
        }[target]

        if value is not None:
            effect_func(target_obj, value)
        else:
            effect_func(target_obj)

    return effect
