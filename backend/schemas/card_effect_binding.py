from pydantic import BaseModel
from typing import Optional

class CardEffectBindingBase(BaseModel):
    card_id: int
    trigger_id: int
    effect_id: int
    condition_id: Optional[int] = None
    max_triggers_per_turn: Optional[int] = None

class CardEffectBindingCreate(CardEffectBindingBase):
    pass

class CardEffectBindingRead(CardEffectBindingBase):
    id: int

    class Config:
        orm_mode = True
