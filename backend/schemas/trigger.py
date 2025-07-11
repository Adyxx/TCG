from pydantic import BaseModel
from typing import Optional

class TriggerBase(BaseModel):
    code: str
    description: Optional[str] = ""

class TriggerCreate(TriggerBase):
    pass

class TriggerRead(TriggerBase):
    id: int

    class Config:
        orm_mode = True
