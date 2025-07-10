
from typing import Optional
from backend.models import Restriction

class RestrictionService:
    @staticmethod
    def get_by_code(code: str) -> Optional[Restriction]:
        try:
            return Restriction.objects.get(code=code)
        except Restriction.DoesNotExist:
            return None

    @staticmethod
    def create(code: str, description: str) -> Restriction:
        restriction, _ = Restriction.objects.get_or_create(code=code, defaults={'description': description})
        return restriction

    @staticmethod
    def list_all():
        return Restriction.objects.all()
