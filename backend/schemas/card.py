from pydantic import BaseModel
from typing import List, Optional

class CardBase(BaseModel):
    name: str
    cost: int
    card_type: str
    color: str
    subtype: Optional[str] = None
    power: Optional[int] = None
    health: Optional[int] = None
    text: Optional[str] = None
    is_character_card: bool = False
    character_id: Optional[int] = None
    ability_ids: List[int] = [] 

class CardCreate(CardBase):
    pass

class CardUpdate(BaseModel):
    name: Optional[str] = None
    cost: Optional[int] = None
    card_type: Optional[str] = None
    color: Optional[str] = None
    subtype: Optional[str] = None
    power: Optional[int] = None
    health: Optional[int] = None
    text: Optional[str] = None
    is_character_card: Optional[bool] = None
    character_id: Optional[int] = None
    ability_ids: Optional[List[int]] = None

class CardInDB(CardBase):
    id: int

    class Config:
        orm_mode = True
