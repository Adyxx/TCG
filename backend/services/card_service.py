from backend.models.card import Card
from backend.schemas.card import CardCreate, CardUpdate
from django.db.models import QuerySet
from typing import List, Optional

class CardService:

    @staticmethod
    def get_all() -> QuerySet[Card]:
        return Card.objects.all()

    @staticmethod
    def get_by_id(card_id: int) -> Optional[Card]:
        return Card.objects.filter(id=card_id).first()

    @staticmethod
    def create(card_in: CardCreate) -> Card:
        card = Card(**card_in.dict())
        card.save()
        return card

    @staticmethod
    def update(card: Card, card_in: CardUpdate) -> Card:
        for field, value in card_in.dict(exclude_unset=True).items():
            setattr(card, field, value)
        card.save()
        return card

    @staticmethod
    def delete(card: Card) -> None:
        card.delete()
