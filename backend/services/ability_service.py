from typing import Optional
from backend.models import Ability, Card
from backend.registry.effects import EFFECT_REGISTRY 


class AbilityService:
    @staticmethod
    def get_ability_by_name(name: str) -> Optional[Ability]:
        try:
            return Ability.objects.get(name=name)
        except Ability.DoesNotExist:
            return None

    @staticmethod
    def get_ability_by_id(ability_id: int) -> Optional[Ability]:
        try:
            return Ability.objects.get(id=ability_id)
        except Ability.DoesNotExist:
            return None

    @staticmethod
    def get_effect_function(script_reference: str):
        if script_reference not in EFFECT_REGISTRY:
            raise ValueError(f"No effect function registered for '{script_reference}'")
        return EFFECT_REGISTRY[script_reference]

    @staticmethod
    def execute_ability(ability: Ability, card: Card):
        """Executes the logic of an ability on a card."""
