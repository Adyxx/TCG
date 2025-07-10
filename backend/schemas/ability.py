from pydantic import BaseModel
from typing import Optional

class AbilityBase(BaseModel):
    name: str
    description: str
    script_reference: str

class AbilityCreate(AbilityBase):
    pass

class AbilityUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    script_reference: Optional[str] = None

class AbilityInDB(AbilityBase):
    id: int

    class Config:
        orm_mode = True
