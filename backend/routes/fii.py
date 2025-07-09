from fastapi import APIRouter, Depends, HTTPException, Response, status
from typing import List
from core.dependencies import get_current_user
from tortoise.exceptions import IntegrityError
from schemas.fii import FiiCreate, FiiOut, FiiPatch
from models.models import Fiis
from services.fii_scraper import FiiScraper


router = APIRouter()

@router.get("/", response_model=List[FiiOut])
async def get_fiis():
    fiis = await Fiis.all()
    return fiis

@router.post("/", response_model=FiiOut)
async def post_fiis(payload: FiiCreate, current_user=Depends(get_current_user)):
    try:
        scraper = FiiScraper(payload.code)
        price = await scraper.get_price()
        dividend = await scraper.get_dividend()

        new_fii = await Fiis.create(
            code=payload.code,
            price=price,
            dividend=dividend,
        )
        return new_fii
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Erro ao criar FII")
    
# @router.patch("/{fii_id}", response_model=FiiOut)
# async def patch_fii(fii_id: int, data: FiiPatch, current_user=Depends(get_current_user)):
#     fii = Fiis.get_or_none(fii_id)
#     if not fii:
#         raise HTTPException(status_code=404, detail="Fii não encontrada")
    
#     if data.code is not None:
#         fii.code = data.code
#     if data.price is not None:
#         fii.price = data.price
#     if data.dividend is not None:
#         fii.dividend = data.dividend
#     if data.quantity is not None:
#         fii.quantity = data.quantity

#     await fii.save()

#     return fii

# @router.delete("/{fii_id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_fii(fii_id: int, current_user=Depends(get_current_user)):
#     fii = Fiis.get_or_none(fii_id)
#     if not fii:
#         raise HTTPException(status_code=404, detail="Fii não encontrada")
    
#     await fii.delete()
#     return Response(status_code=status.HTTP_204_NO_CONTENT)