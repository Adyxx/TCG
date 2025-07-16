from backend.engine.trigger_helper import resolve_effect_target

def build(card, owner, binding):
    effect_func, _ = binding.effect.get_executable()
    value = binding.value

    def effect(**kwargs):
        if kwargs.get("card") != card:
            return

        try:
            target_obj = resolve_effect_target(owner, card, binding)
        except ValueError as e:
            print(f"⚠️ {e}")
            return

        effect_func(source=card, target=target_obj, value=value)

    return effect
