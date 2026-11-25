from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import chat, contracts, documents, health
from app.config import get_settings

app = FastAPI(title="ИИ-юрист API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_settings().cors_origin_list,
    allow_methods=["*"],
    allow_headers=["*"],
)

for module in (health, chat, contracts, documents):
    app.include_router(module.router, prefix="/api")
