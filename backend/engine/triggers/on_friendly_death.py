from backend.engine.trigger_helper import resolve_effect_target

def build(card, owner, binding):
    effect_func, _ = binding.effect.get_executable()
    value = binding.value
    expected_zone = getattr(binding.trigger, "zone", None)

    def effect(**kwargs):
        died_card = kwargs.get("died_card")
        if died_card is None:
            return

        if died_card.owner != owner:
            return

        if expected_zone and card.zone != expected_zone:
            return

        try:
            target_obj = resolve_effect_target(owner, card, binding)
        except ValueError as e:
            print(f"⚠️ {e}")
            return

        effect_func(source=card, target=target_obj, value=value)

    return effect
