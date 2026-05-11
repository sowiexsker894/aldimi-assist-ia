from fastapi import APIRouter

router = APIRouter()


@router.get("/health", summary="Estado del servicio")
def health() -> dict[str, str]:
    return {"status": "ok"}
