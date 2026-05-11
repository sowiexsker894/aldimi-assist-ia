from fastapi import APIRouter

from app.api.v1.endpoints import health, patients, stub_ai

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(patients.router, prefix="/patients", tags=["patients"])
api_router.include_router(stub_ai.router, prefix="/stub", tags=["stub-ia"])
