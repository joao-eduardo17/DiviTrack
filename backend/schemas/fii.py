from pydantic import BaseModel

class FiiCreate(BaseModel):
    code: str
    price: float
    dividend: float
    user_id: int

class FiiOut(BaseModel):
    id: int
    code: str
    price: float
    dividend: float
    user_id: int

    class Config:
        from_attributes = True
