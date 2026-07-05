from fastapi import APIRouter

from app.api.v1.endpoints import admin_volunteers, auth, documents, health, patients, stub_ai

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(
    admin_volunteers.router, prefix="/admin", tags=["admin"]
)
api_router.include_router(patients.router, prefix="/patients", tags=["patients"])
api_router.include_router(documents.router, prefix="/documents", tags=["documents"])
api_router.include_router(stub_ai.router, prefix="/stub", tags=["stub-ia"])
