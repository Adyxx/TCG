from backend.registry.effects import EFFECT_REGISTRY
from backend.registry.conditions import CONDITION_REGISTRY
from backend.registry.restrictions import RESTRICTION_REGISTRY


def execute_trigger(card, trigger_code, player=None):
    if card:
        print(f"[CARD] Checking trigger {trigger_code} on card {card.name}")
        bindings = card.effect_bindings.filter(trigger__script_reference=trigger_code)

        for binding in bindings:
            print(f"🔗 Binding {binding} → Effect: {binding.effect.script_reference}, Condition: {binding.condition}, Restriction: {binding.restriction}")
            if binding.restriction:
                restriction_func = RESTRICTION_REGISTRY.get(binding.restriction.script_reference)
                if restriction_func and not restriction_func(card, binding.id):
                    print("🚫 Restriction blocked this effect.")
                    continue

            if binding.condition:
                print(f"🔍 Found condition: {binding.condition.script_reference}")
                condition_func = CONDITION_REGISTRY.get(binding.condition.script_reference)
                if condition_func:
                    result = condition_func(board_card)
                    print(f"🔍 Condition returned {result}")
                    if not result:
                        print("🟡 Condition not met.")
                        continue
                else:
                    print(f"❌ No condition func found for {binding.condition.script_reference}")


            effect_func = EFFECT_REGISTRY.get(binding.effect.script_reference)
            if effect_func:
                print(f"✅ Executing: {binding.effect.script_reference}")
                effect_func(card)
            else:
                print(f"❌ Effect '{binding.effect.script_reference}' not found.")

    elif player:
        print(f"[PLAYER] Checking trigger {trigger_code} on all cards of {player.name}")
        for board_card in player.board:
            bindings = board_card.effect_bindings.filter(trigger__script_reference=trigger_code)

            for binding in bindings:
                print(f"🔗 Binding {binding} → Effect: {binding.effect.script_reference}, Condition: {binding.condition}, Restriction: {binding.restriction}")
                
                if binding.restriction:
                    restriction_func = RESTRICTION_REGISTRY.get(binding.restriction.script_reference)
                    if restriction_func and not restriction_func(board_card, binding.id):
                        print("🚫 Restriction blocked this effect.")
                        continue

                if binding.condition:
                    print(f"🔍 Found condition: {binding.condition.script_reference}")
                    condition_func = CONDITION_REGISTRY.get(binding.condition.script_reference)
                    if condition_func:
                        result = condition_func(board_card)
                        print(f"🔍 Condition returned {result}")
                        if not result:
                            print("🟡 Condition not met.")
                            continue
                    else:
                        print(f"❌ No condition func found for {binding.condition.script_reference}")

                effect_func = EFFECT_REGISTRY.get(binding.effect.script_reference)
                if effect_func:
                    print(f"✅ Executing: {binding.effect.script_reference}")
                    effect_func(board_card)
                else:
                    print(f"❌ Effect '{binding.effect.script_reference}' not found.")
