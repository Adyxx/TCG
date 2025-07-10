from typing import Optional, List
from backend.models import Condition

class ConditionService:
    @staticmethod
    def get_all() -> List[Condition]:
        return Condition.objects.all()

    @staticmethod
    def get_by_id(condition_id: int) -> Optional[Condition]:
        return Condition.objects.filter(id=condition_id).first()

    @staticmethod
    def create(**kwargs) -> Condition:
        return Condition.objects.create(**kwargs)

    @staticmethod
    def update(condition_id: int, **kwargs) -> Optional[Condition]:
        condition = ConditionService.get_by_id(condition_id)
        if condition:
            for key, value in kwargs.items():
                setattr(condition, key, value)
            condition.save()
        return condition

    @staticmethod
    def delete(condition_id: int) -> bool:
        condition = ConditionService.get_by_id(condition_id)
        if condition:
            condition.delete()
            return True
        return False
