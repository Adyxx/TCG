from typing import Optional, List
from backend.models import CardEffectBinding

class CardEffectBindingService:
    @staticmethod
    def get_all() -> List[CardEffectBinding]:
        return CardEffectBinding.objects.all()

    @staticmethod
    def get_by_id(binding_id: int) -> Optional[CardEffectBinding]:
        return CardEffectBinding.objects.filter(id=binding_id).first()

    @staticmethod
    def create(**kwargs) -> CardEffectBinding:
        return CardEffectBinding.objects.create(**kwargs)

    @staticmethod
    def update(binding_id: int, **kwargs) -> Optional[CardEffectBinding]:
        binding = CardEffectBindingService.get_by_id(binding_id)
        if binding:
            for key, value in kwargs.items():
                setattr(binding, key, value)
            binding.save()
        return binding

    @staticmethod
    def delete(binding_id: int) -> bool:
        binding = CardEffectBindingService.get_by_id(binding_id)
        if binding:
            binding.delete()
            return True
        return False
