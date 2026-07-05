from fastapi import APIRouter, HTTPException
from openai import OpenAIError
from pydantic import BaseModel, Field, model_validator

from app.api.deps import VisionServiceDep
from app.schemas.analyze_response import AnalyzeResponse
from app.schemas.dni_extracted import DniExtracted
from app.schemas.document_type import DocumentType
from app.services.vision_exceptions import VisionRejectedError, VisionRequestError

router = APIRouter()


class AnalyzeRequest(BaseModel):
    document_type: DocumentType = Field(
        default="dni",
        description="Tipo de documento esperado: dni, receta o boleta.",
    )
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
    summary="Extracción documental (OpenCV + gatekeeper + LLM)",
    description=(
        "Preprocesa imágenes, evalúa gatekeeper (stub), extrae JSON según document_type. "
        "Errores 400 (entrada), 413 (límites), 422 (gatekeeper), 502 (modelo / JSON inválido)."
    ),
)
def post_analyze(
    body: AnalyzeRequest,
    svc: VisionServiceDep,
) -> AnalyzeResponse:
    _ = body.hint
    images = _collect_images(body)
    try:
        result = svc.analyze(body.document_type, images)
    except VisionRejectedError as exc:
        raise HTTPException(
            status_code=422,
            detail={
                "status": "rejected",
                "rejection": {"code": exc.code, "message": exc.message},
            },
        ) from exc
    except VisionRequestError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail) from exc
    except OpenAIError as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc

    legacy_data: DniExtracted | None = None
    if body.document_type == "dni":
        legacy_data = DniExtracted.model_validate(result.draft)

    return AnalyzeResponse(
        status="accepted",
        document_type=result.document_type,
        draft=result.draft,
        warnings=result.warnings,
        metadata=result.metadata,
        data=legacy_data,
    )
