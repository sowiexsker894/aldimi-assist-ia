from fastapi import APIRouter

from app.api.v1.endpoints import chat, emotions, health

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(chat.router, tags=["chat"])
api_router.include_router(emotions.router, tags=["emotions"])