from backend.models.deck import Deck
from backend.schemas.deck import DeckCreate, DeckUpdate
from typing import Optional

class DeckService:

    @staticmethod
    def get_all():
        return Deck.objects.all()

    @staticmethod
    def get_by_id(deck_id: int) -> Optional[Deck]:
        return Deck.objects.filter(id=deck_id).first()

    @staticmethod
    def create(deck_in: DeckCreate) -> Deck:
        deck = Deck(**deck_in.dict())
        deck.save()
        return deck

    @staticmethod
    def update(deck: Deck, deck_in: DeckUpdate) -> Deck:
        for field, value in deck_in.dict(exclude_unset=True).items():
            setattr(deck, field, value)
        deck.save()
        return deck

    @staticmethod
    def delete(deck: Deck) -> None:
        deck.delete()
