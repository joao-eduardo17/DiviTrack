from tortoise.contrib.fastapi import register_tortoise
from fastapi.middleware.cors import CORSMiddleware
from routes import user, fii, auth, wallet
from dotenv import load_dotenv
from fastapi import FastAPI
import os


app = FastAPI()
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(fii.router, prefix="/fiis", tags=["FIIs"])
app.include_router(wallet.router, prefix="/wallet", tags=["Wallet"])

load_dotenv()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://your-site.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_tortoise(
    app,
    db_url=os.getenv("DATABASE_URL"),  # URL of where database are
    modules={"models": ["models.models"]},  # path where the models are
    generate_schemas=True,  # false on deploy
    add_exception_handlers=True,
)
