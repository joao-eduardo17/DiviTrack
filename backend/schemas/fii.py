from pydantic import BaseModel
from typing import Optional


class FiiCreate(BaseModel):
    code: str
    price: float
    dividend: float
    quantity: Optional[int] = None  # Campo opcional

class FiiOut(BaseModel):
    id: int
    code: str
    price: float
    dividend: float
    quantity: int

    class Config:
        from_attributes = True

class FiiPatch(BaseModel):
    code: str
    price: float
    dividend: float
    quantity: int