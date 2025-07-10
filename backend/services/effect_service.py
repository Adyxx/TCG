from typing import Optional, List
from backend.models import Effect

class EffectService:
    @staticmethod
    def get_all() -> List[Effect]:
        return Effect.objects.all()

    @staticmethod
    def get_by_id(effect_id: int) -> Optional[Effect]:
        return Effect.objects.filter(id=effect_id).first()

    @staticmethod
    def create(**kwargs) -> Effect:
        return Effect.objects.create(**kwargs)

    @staticmethod
    def update(effect_id: int, **kwargs) -> Optional[Effect]:
        effect = EffectService.get_by_id(effect_id)
        if effect:
            for key, value in kwargs.items():
                setattr(effect, key, value)
            effect.save()
        return effect

    @staticmethod
    def delete(effect_id: int) -> bool:
        effect = EffectService.get_by_id(effect_id)
        if effect:
            effect.delete()
            return True
        return False
