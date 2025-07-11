from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class MatchBase(BaseModel):
    player1_id: int
    player2_id: int
    winner_id: Optional[int] = None
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None

class MatchCreate(MatchBase):
    pass

class MatchUpdate(MatchBase):
    pass

class MatchInDB(MatchBase):
    id: int

    class Config:
        orm_mode = True
