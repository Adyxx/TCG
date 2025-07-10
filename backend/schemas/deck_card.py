from pydantic import BaseModel
from typing import Optional

class DeckCardBase(BaseModel):
    deck_id: int
    card_id: int
    quantity: int = 1

class DeckCardCreate(DeckCardBase):
    pass

class DeckCardUpdate(BaseModel):
    quantity: int

class DeckCardInDB(DeckCardBase):
    id: int

    class Config:
        orm_mode = True
