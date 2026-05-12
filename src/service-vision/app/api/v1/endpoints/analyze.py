from fastapi import APIRouter, HTTPException
from openai import OpenAIError
from pydantic import BaseModel, Field, model_validator

from app.api.deps import VisionServiceDep
from app.schemas.dni_extracted import DniExtracted
from app.services.vision_exceptions import VisionRequestError

router = APIRouter()


class AnalyzeRequest(BaseModel):
    hint: str | None = Field(default=None, max_length=2000)
    image_base64: str | None = Field(
        default=None,
        description="Una imagen en base64 (legacy); puede combinarse con images_base64.",
    )
    images_base64: list[str] = Field(
        default_factory=list,
        description="Una o más imágenes en base64 (con o sin prefijo data URL).",
    )

    @model_validator(mode="after")
    def at_least_one_image_source(self) -> "AnalyzeRequest":
        has_legacy = bool(self.image_base64 and self.image_base64.strip())
        has_list = any(s and str(s).strip() for s in self.images_base64)
        if not has_legacy and not has_list:
            raise ValueError(
                "Debe enviarse image_base64 y/o images_base64 con al menos una imagen no vacía"
            )
        return self


class AnalyzeResponse(BaseModel):
    data: DniExtracted


def _collect_images(body: AnalyzeRequest) -> list[str]:
    merged: list[str] = []
    for raw in body.images_base64:
        if raw and str(raw).strip():
            merged.append(str(raw).strip())
    if body.image_base64 and body.image_base64.strip():
        merged.append(body.image_base64.strip())
    return merged


@router.post(
    "/analyze",
    response_model=AnalyzeResponse,
    summary="Extracción DNI (OpenCV + Azure multimodal)",
    description=(
        "Preprocesa una o más imágenes y llama al modelo con el prompt de extractor DNI. "
        "Errores 400 (entrada), 413 (límites de tamaño), 502 (modelo / JSON inválido)."
    ),
)
def post_analyze(
    body: AnalyzeRequest,
    svc: VisionServiceDep,
) -> AnalyzeResponse:
    _ = body.hint
    images = _collect_images(body)
    try:
        data = svc.extract_dni(images)
    except VisionRequestError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail) from exc
    except OpenAIError as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc
    return AnalyzeResponse(data=data)
