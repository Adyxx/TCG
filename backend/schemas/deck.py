from pydantic import BaseModel
from typing import Optional

class DeckBase(BaseModel):
    user_id: int
    name: str
    description: Optional[str] = None

class DeckCreate(DeckBase):
    pass

class DeckUpdate(DeckBase):
    pass

class DeckInDB(DeckBase):
    id: int

    class Config:
        orm_mode = True
