from pydantic import BaseModel
from typing import Optional

class CharacterBase(BaseModel):
    name: str
    color: str
    subtype: str
    solo_hp: int
    solo_energy: int
    solo_passive: str
    partner_hp: int
    partner_energy: int
    partner_passive: str

class CharacterCreate(CharacterBase):
    pass

class CharacterUpdate(CharacterBase):
    pass

class CharacterInDB(CharacterBase):
    id: int

    class Config:
        orm_mode = True
