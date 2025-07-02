from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from jose.exceptions import ExpiredSignatureError
from jose import JWTError, jwt
import os


load_dotenv()

# Chave secreta para assinar o token
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise ValueError("Token inválido: sem ID")
        return int(user_id)
    except ExpiredSignatureError:
        raise ValueError("Token expirado")
    except JWTError:
        raise ValueError("Token inválido")