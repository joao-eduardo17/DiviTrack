from pydantic import BaseModel


class UserFiiOut(BaseModel):
    id: int
    user: int
    fii: int
    