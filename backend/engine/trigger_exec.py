import inspect
from backend.registry.effects import EFFECT_REGISTRY
from backend.registry.conditions import CONDITION_REGISTRY
from backend.registry.restrictions import RESTRICTION_REGISTRY
from backend.registry.character_abilities import CHARACTER_ABILITY_REGISTRY, CHARACTER_ABILITY_METADATA

def execute_trigger(card=None, trigger_code=None, player=None):
    if not trigger_code:
        return

    # === 1. Card-specific effect trigger ===
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
                condition_func = CONDITION_REGISTRY.get(binding.condition.script_reference)
                if condition_func:
                    result = condition_func(card)
                    print(f"🔍 Condition returned {result}")
                    if not result:
                        print("🟡 Condition not met.")
                        continue
                else:
                    print(f"❌ No condition func found for {binding.condition.script_reference}")

            effect_func = EFFECT_REGISTRY.get(binding.effect.script_reference)
            if effect_func:
                print(f"✅ Executing: {binding.effect.script_reference}")
                try:
                    if len(inspect.signature(effect_func).parameters) >= 2:
                        effect_func(card, binding.value)
                    else:
                        effect_func(card)
                except Exception as e:
                    print(f"❌ Error while executing effect: {e}")

    # === 2. Player-wide trigger handling ===
    elif player:
        print(f"[PLAYER] Checking trigger {trigger_code} on all cards and abilities of {player.name}")

        # 2A. Run effects on board cards
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
                    try:
                        if len(inspect.signature(effect_func).parameters) >= 2:
                            effect_func(board_card, binding.value)
                        else:
                            effect_func(board_card)
                    except Exception as e:
                        print(f"❌ Error while executing effect: {e}")

        # 2B. Run character passive abilities
        for character in filter(None, [getattr(player.deck_model, "character", None),
                                       getattr(player.deck_model, "partner_character", None)]):
            ability_ref = character.passive_ability_ref
            if not ability_ref:
                continue

            meta = CHARACTER_ABILITY_METADATA.get(ability_ref)
            if not meta:
                print(f"⚠️ No metadata for passive ability '{ability_ref}'")
                continue

            if meta.get("type") != "passive" or meta.get("trigger") != trigger_code:
                continue

            ability_func = CHARACTER_ABILITY_REGISTRY.get(ability_ref)
            if ability_func:
                print(f"🌟 Passive ability '{ability_ref}' triggered for {character.name}")
                try:
                    ability_func(player)
                except Exception as e:
                    print(f"❌ Error in passive ability '{ability_ref}': {e}")

        # 2C. Run class trait if triggered
        if player.class_trait:
            trait_trigger = player.class_trait.get("trigger")
            if trait_trigger == trigger_code:
                usage_limit = player.class_trait.get("uses_per_turn", 1)
                if getattr(player, "_class_trait_uses_this_turn", 0) < usage_limit:
                    print(f"🧬 Class trait triggered for {player.name}")
                    try:
                        player.class_trait["function"](player)
                        player._class_trait_uses_this_turn += 1
                    except Exception as e:
                        print(f"❌ Error in class trait: {e}")
