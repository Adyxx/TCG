from backend.registry.effects import EFFECT_REGISTRY
from backend.registry.conditions import CONDITION_REGISTRY

from backend.registry.restrictions import RESTRICTION_REGISTRY

class AbilityService:
    @staticmethod
    def execute_effect(effect, card):
        func = EFFECT_REGISTRY.get(effect.script_reference)
        if not func:
            raise ValueError(f"Effect '{effect.name}' not registered.")
        return func(card)

    @staticmethod
    def check_condition(binding, card) -> bool:
        if not binding.condition:
            return True
        func = CONDITION_REGISTRY.get(binding.condition.script_reference)
        if not func:
            raise ValueError(f"Condition '{binding.condition}' not registered.")
        return func(card)

    @staticmethod
    def check_restriction(binding, card) -> bool:
        if not binding.restriction:
            return True
        func = RESTRICTION_REGISTRY.get(binding.restriction.code)
        if not func:
            raise ValueError(f"Restriction '{binding.restriction.code}' not registered.")
        return func(card, binding.id)

    @staticmethod
    def trigger(card, trigger_code):
        for binding in card.effect_bindings.filter(trigger__code=trigger_code):
            if (
                AbilityService.check_condition(binding, card)
                and AbilityService.check_restriction(binding, card)
            ):
                AbilityService.execute_effect(binding.effect, card)
