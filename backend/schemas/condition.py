from pydantic import BaseModel
from typing import Optional

class ConditionBase(BaseModel):
    name: str
    script_reference: str
    description: Optional[str] = ""

class ConditionCreate(ConditionBase):
    pass

class ConditionRead(ConditionBase):
    id: int

    class Config:
        orm_mode = True
