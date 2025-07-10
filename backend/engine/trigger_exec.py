from backend.registry.effects import EFFECT_REGISTRY
from backend.registry.conditions import CONDITION_REGISTRY
from backend.registry.restrictions import RESTRICTION_REGISTRY


def execute_trigger(card, trigger_code, player=None):
    if card:
        bindings = card.effect_bindings.filter(trigger__code=trigger_code)
    elif player:
        bindings = []
        for card in player.hand + player.deck + player.graveyard:
            bindings.extend(card.effect_bindings.filter(trigger__code=trigger_code))
    else:
        return

    for binding in bindings:
        if binding.restriction:
            restriction_func = RESTRICTION_REGISTRY.get(binding.restriction.code)
            if restriction_func and not restriction_func(card, binding.id):
                print("🚫 Restriction blocked this effect.")
                continue

        if binding.condition:
            condition_func = CONDITION_REGISTRY.get(binding.condition.script_reference)
            if condition_func and not condition_func(card):
                print("🟡 Condition not met.")
                continue

        effect_func = EFFECT_REGISTRY.get(binding.effect.script_reference)
        if effect_func:
            print(f"✅ Executing: {binding.effect.script_reference}")
            effect_func(card)
        else:
            print(f"❌ Effect '{binding.effect.script_reference}' not found.")
