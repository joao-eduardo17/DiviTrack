from fastapi import APIRouter, Depends
from core.dependencies import get_current_user
from models.models import UserFiis


router = APIRouter()

@router.get("/", response_model="")
async def get_user_fiis(current_user=Depends(get_current_user)):
    fiis = await UserFiis.all(user=current_user.id)
    return fiis