from pydantic import BaseModel

class RestrictionSchema(BaseModel):
    id: int
    code: str
    description: str

    class Config:
        orm_mode = True
