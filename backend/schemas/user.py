from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True

class UserPatch(BaseModel):
    name: str | None = None
    email: str | None = None
    password: str | None = None
