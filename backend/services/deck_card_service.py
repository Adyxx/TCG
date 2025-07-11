from backend.models.deck_card import DeckCard
from backend.schemas.deck_card import DeckCardCreate, DeckCardUpdate
from typing import Optional

class DeckCardService:

    @staticmethod
    def get_all():
        return DeckCard.objects.all()

    @staticmethod
    def get_by_id(deck_card_id: int) -> Optional[DeckCard]:
        return DeckCard.objects.filter(id=deck_card_id).first()

    @staticmethod
    def create(deck_card_in: DeckCardCreate) -> DeckCard:
        deck_card = DeckCard(**deck_card_in.dict())
        deck_card.save()
        return deck_card

    @staticmethod
    def update(deck_card: DeckCard, deck_card_in: DeckCardUpdate) -> DeckCard:
        for field, value in deck_card_in.dict(exclude_unset=True).items():
            setattr(deck_card, field, value)
        deck_card.save()
        return deck_card

    @staticmethod
    def delete(deck_card: DeckCard) -> None:
        deck_card.delete()
