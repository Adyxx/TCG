
def build(card, owner, binding):
    effect_func = binding.effect.get_executable()
    value = binding.value

    def effect(**kwargs):
        if kwargs.get("card") != card:
            return
        print(f"⚔️ [on_attack] Triggering for {card.name}")
        effect_func(card, value) if value is not None else effect_func(card)

    return effect
