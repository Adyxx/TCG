from typing import Optional, List
from backend.models import Trigger

class TriggerService:
    @staticmethod
    def get_all() -> List[Trigger]:
        return Trigger.objects.all()

    @staticmethod
    def get_by_id(trigger_id: int) -> Optional[Trigger]:
        return Trigger.objects.filter(id=trigger_id).first()

    @staticmethod
    def create(**kwargs) -> Trigger:
        return Trigger.objects.create(**kwargs)

    @staticmethod
    def update(trigger_id: int, **kwargs) -> Optional[Trigger]:
        trigger = TriggerService.get_by_id(trigger_id)
        if trigger:
            for key, value in kwargs.items():
                setattr(trigger, key, value)
            trigger.save()
        return trigger

    @staticmethod
    def delete(trigger_id: int) -> bool:
        trigger = TriggerService.get_by_id(trigger_id)
        if trigger:
            trigger.delete()
            return True
        return False
