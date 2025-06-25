from fastapi import APIRouter, Depends, HTTPException, Response, status
from core.dependencies import get_current_user
from tortoise.exceptions import IntegrityError
from schemas.fii import FiiCreate, FiiOut, FiiPatch
from models.models import Fiis


router = APIRouter()

@router.post("/", response_model=FiiOut)
async def post_fiis(fii: FiiCreate, current_user=Depends(get_current_user)):
    try:
        new_fii = await Fiis.create(
            code=fii.code,
            price=fii.price,
            dividend=fii.dividend,
            quantity=fii.quantity,
            user_id=current_user.id
        )
        return new_fii
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Erro ao criar FII")
    
@router.patch("/{fii_id}", response_model=FiiOut)
async def patch_fii(fii_id: int, data: FiiPatch, current_user=Depends(get_current_user)):
    fii = Fiis.get_or_none(fii_id)
    if not fii:
        raise HTTPException(status_code=404, detail="Fii não encontrada")
    
    if data.code is not None:
        fii.code = data.code
    if data.price is not None:
        fii.price = data.price
    if data.dividend is not None:
        fii.dividend = data.dividend
    if data.quantity is not None:
        fii.quantity = data.quantity

    await fii.save()

    return fii

@router.delete("/{fii_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_fii(fii_id: int, current_user=Depends(get_current_user)):
    fii = Fiis.get_or_none(fii_id)
    if not fii:
        raise HTTPException(status_code=404, detail="Fii não encontrada")
    
    await fii.delete()
    return Response(status_code=status.HTTP_204_NO_CONTENT)