def build(card, owner, binding):
    effect_func, target = binding.effect.get_executable()
    value = binding.value

    def effect(**kwargs):
        if kwargs.get("card") != card:
            return
        #print(f"⌛ [on_turn_start] Triggering for {card.name}")
        
        target_obj = {
            "card": card,
            "player": owner,
        }[target]

        if value is not None:
            effect_func(target_obj, value)
        else:
            effect_func(target_obj)

    return effect
