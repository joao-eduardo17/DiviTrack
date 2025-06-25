from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from core.security import decode_access_token
from models.models import Users

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")  # URL do login

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        user_id = decode_access_token(token)
        user = await Users.get_or_none(id=user_id)
        if not user:
            raise HTTPException(status_code=401, detail="Usuário não encontrado")
        return user
    except ValueError:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")
