def resolve_effect_target(owner, card, binding):
    from backend.engine.actions import choose_target
    from backend.registry.effects import EFFECT_REGISTRY

    script_ref = binding.effect.script_reference
    target_type = EFFECT_REGISTRY.get(script_ref, {}).get("target", None)

    if target_type == "card":
        return card
    elif target_type == "player":
        return owner
    elif target_type is None:
        if not binding.target_spec:
            raise ValueError(f"Effect '{script_ref}' requires a target_spec, but none provided.")
        return choose_target(owner, binding.target_spec)
    else:
        raise ValueError(f"Unknown target type '{target_type}' in EFFECT_REGISTRY for effect '{script_ref}'")
