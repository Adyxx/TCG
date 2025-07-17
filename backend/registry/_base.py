from backend.registry.conditions import evaluate_condition

class AbilityRegistry:
    def __init__(self):
        self.registry = {}
        self.metadata = {}

    def register(self, ref, *, type, description, trigger=None, cooldown=None,
                 condition=None, cost=None, needs_target=None,
                 effect_type=None, target_spec=None, **kwargs):
        def decorator(func):
            self.registry[ref] = func
            self.metadata[ref] = {
                "type": type,
                "description": description,
                "trigger": trigger,
                "cooldown": cooldown,
                "condition": condition,
                "cost": cost,
                "needs_target": needs_target,
                "effect_type": effect_type,
                "target_spec": target_spec,
                "function": func,
                **kwargs
            }
            return func
        return decorator

    def build_wrapped_passive(self, player, ref, attr_prefix):
        meta = self.get_metadata(ref)
        func = self.get_function(ref)

        if not meta or not func:
            print(f"⚠️ Invalid passive ability: {ref}")
            return None

        trigger = meta.get("trigger")
        condition = meta.get("condition")
        cooldown = meta.get("cooldown")

        def wrapped(**kwargs):
            if cooldown:
                if getattr(player, "cooldowns", {}).get(ref, 0) > 0:
                    print(f"🧊 Cooldown active for {ref} ({player.name})")
                    return

            subject = kwargs.get("card", player)

            if not evaluate_condition(condition, subject, ref=ref):
                print(f"⚠️ Condition blocked {ref} ({subject.name})")
                return

            print(f"⚡ Triggered passive: {ref} → {player.name}")
            func(player)

            if not hasattr(player, "turn_usage"):
                player.turn_usage = {}

            player.turn_usage[ref] = player.turn_usage.get(ref, 0) + 1

            if cooldown:
                if not hasattr(player, "cooldowns"):
                    player.cooldowns = {}
                player.cooldowns[ref] = cooldown

        return trigger, wrapped

    def get_metadata(self, ref):
        return self.metadata.get(ref)

    def get_function(self, ref):
        return self.registry.get(ref)

    def items(self):
        return self.metadata.items()

    def keys(self):
        return self.metadata.keys()

    def values(self):
        return self.metadata.values()
