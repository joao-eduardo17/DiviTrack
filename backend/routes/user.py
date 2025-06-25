from fastapi import APIRouter, HTTPException, Response, status, Depends
from schemas.user import UserCreate, UserOut, UserPatch
from core.dependencies import get_current_user
from models.models import Users
import bcrypt


router = APIRouter()

@router.get("/", response_model=list[UserOut])
async def get_users():
    users = await Users.all()
    return users

@router.get("/me")
async def get_logged_user(current_user: Users = Depends(get_current_user)):
    return {"id": current_user.id, "email": current_user.email}

@router.post("/", response_model=UserOut)
async def post_user(user: UserCreate):
    existing_user = await Users.get_or_none(email=user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email já está em uso")

    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())

    user_dict = user.model_dump()
    user_dict["password"] = hashed_password.decode()
    new_user = await Users.create(**user_dict)

    return new_user

@router.patch("/{user_id}", response_model=UserOut)
async def patch_user(user_id: int, data: UserPatch, current_user: Users = Depends(get_current_user)):
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Acesso negado")
    
    existing_user = await Users.get_or_none(id=user_id)
    if not existing_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    if data.name is not None:
        existing_user.name = data.name
    if data.email is not None:
        existing_user.email = data.email
    if data.password is not None:
        existing_user.password = data.password
    
    await existing_user.save()

    return existing_user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, current_user: Users = Depends(get_current_user)):
    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Acesso negado")
    
    user = await Users.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    await user.delete()
    return Response(status_code=status.HTTP_204_NO_CONTENT)