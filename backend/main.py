from tortoise.contrib.fastapi import register_tortoise
from dotenv import load_dotenv
from routes import user, fii, auth
from fastapi import FastAPI
import os


app = FastAPI()
app.include_router(user.router, prefix="/users")
app.include_router(fii.router, prefix="/fii")
app.include_router(auth.router, prefix="/auth")

load_dotenv()

register_tortoise(
    app,
    db_url=os.getenv("DATABASE_URL"),  # ou outro banco
    modules={"models": ["models.models"]},  # caminho onde estão os models
    generate_schemas=True,  # cria as tabelas automaticamente (em dev)
    add_exception_handlers=True,
)

