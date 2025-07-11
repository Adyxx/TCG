from pydantic import BaseModel
from typing import Optional

class EffectBase(BaseModel):
    name: str
    description: Optional[str] = ""
    script_reference: str

class EffectCreate(EffectBase):
    pass

class EffectRead(EffectBase):
    id: int

    class Config:
        orm_mode = True
