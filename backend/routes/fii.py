from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_fiis():
    return [{"id": 1, "name": "João"}]

