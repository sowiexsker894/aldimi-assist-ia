from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.api.deps import VisionServiceDep

router = APIRouter()


class AnalyzeRequest(BaseModel):
    hint: str | None = Field(default=None, max_length=2000)
    image_base64: str | None = Field(
        default=None,
        max_length=2_000_000,
        description="Opcional; reservado para futura inferencia (Base64).",
    )


class AnalyzeResponse(BaseModel):
    result: str


@router.post(
    "/analyze",
    response_model=AnalyzeResponse,
    summary="Análisis de imagen (stub)",
    description="Contrato mínimo hasta integrar modelo / pipeline de visión.",
)
def post_analyze(
    body: AnalyzeRequest,
    svc: VisionServiceDep,
) -> AnalyzeResponse:
    return AnalyzeResponse(result=svc.analyze_stub(hint=body.hint, has_image=bool(body.image_base64)))
