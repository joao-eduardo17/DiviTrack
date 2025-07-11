from pydantic import BaseModel
from schemas.fii import FiiOut


class WalletOut(BaseModel):
    id: int
    fii: FiiOut
    quantity: int

    class Config:
        from_attributes = True

class WalletCreate(BaseModel):
    fii_id: int
    quantity: int


    