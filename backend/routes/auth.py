from fastapi import APIRouter, HTTPException
from schemas.token import RegisterSchema, LoginSchema, TokenResponse
from schemas.user import UserOut
from models.models import Users
from core.security import create_access_token
import bcrypt


router = APIRouter()

@router.post("/", response_model=UserOut)
async def post_user(user: RegisterSchema):
    existing_user = await Users.get_or_none(email=user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email já está em uso")

    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())

    user_dict = user.model_dump()
    user_dict["password"] = hashed_password.decode()
    new_user = await Users.create(**user_dict)

    return new_user

@router.post("/login", response_model=TokenResponse)
async def login(data: LoginSchema):
    user = await Users.get_or_none(email=data.email)
    if not user or not bcrypt.checkpw(data.password.encode(), user.password.encode()):
        raise HTTPException(status_code=401, detail="Email ou senha inválidos")

    token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": token}
