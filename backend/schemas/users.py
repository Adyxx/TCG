from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    username: str
    email: Optional[str] = None
    rank: int = 0

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[str] = None
    rank: Optional[int] = None
    password: Optional[str] = None

class UserInDB(UserBase):
    id: int

    class Config:
        orm_mode = True
