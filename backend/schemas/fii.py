from pydantic import BaseModel
from typing import Optional


class FiiCreate(BaseModel):
    code: str

class FiiOut(BaseModel):
    id: int
    code: str
    price: float
    dividend: float

    class Config:
        from_attributes = True

class FiiPatch(BaseModel):
    code: str
    price: float
    dividend: float
    quantity: int