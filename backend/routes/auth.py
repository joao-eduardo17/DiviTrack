from fastapi import APIRouter, HTTPException, status
from schemas.token import LoginSchema, TokenResponse
from models.models import Users
from core.security import create_access_token
import bcrypt

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
async def login(data: LoginSchema):
    user = await Users.get_or_none(email=data.email)
    if not user or not bcrypt.checkpw(data.password.encode(), user.password.encode()):
        raise HTTPException(status_code=401, detail="Email ou senha inválidos")

    token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": token}
