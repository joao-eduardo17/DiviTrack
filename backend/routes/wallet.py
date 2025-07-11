from fastapi import APIRouter, Depends, HTTPException, Response, status
from core.dependencies import get_current_user
from tortoise.exceptions import IntegrityError
from models.models import Wallets
from schemas.wallet import WalletCreate, WalletOut
from typing import List


router = APIRouter()

@router.get("/", response_model=List[WalletOut])
async def get_user_fiis(current_user=Depends(get_current_user)):
    fiis = await Wallets.filter(user=current_user.id).prefetch_related("fii")
    return fiis

@router.post("/", response_model=WalletOut)
async def post_user_fiis(payload: WalletCreate, current_user=Depends(get_current_user)):
    verify_fii = await Wallets.get_or_none(user_id=current_user.id, fii_id=payload.fii_id)
    if verify_fii:
        raise HTTPException(status_code=409, detail="O código do FII informado já existe")
    
    try:
        new_wallet = await Wallets.create(
            fii_id=payload.fii_id,
            user_id=current_user.id,
            quantity=payload.quantity
        )
        return Response(status_code=status.HTTP_201_CREATED)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Erro ao criar wallet")

