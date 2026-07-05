import base64
import json
import re
import time
from typing import Any

from pydantic import BaseModel, ValidationError

from app.core.config import Settings
from app.infrastructure.gatekeeper.protocols import GatekeeperPort
from app.infrastructure.image_preprocess import preprocess_to_jpeg_data_url, strip_data_url_prefix
from app.infrastructure.llm.protocols import VisionCompletionClient
from app.schemas.analyze_response import AnalyzeMetadata, AnalyzeResultAccepted
from app.schemas.document_type import DocumentType
from app.schemas.dni_extracted import DniExtracted
from app.schemas.receta_extracted import RecetaExtracted
from app.schemas.recibo_extracted import ReciboExtracted
from app.services.document_validators import get_validator
from app.services.vision_exceptions import VisionRejectedError, VisionRequestError


_CODE_FENCE_START = re.compile(r"^\s*```(?:json)?\s*", re.IGNORECASE)
_CODE_FENCE_END = re.compile(r"\s*```\s*$")

_SCHEMA_BY_TYPE: dict[DocumentType, type[BaseModel]] = {
    "dni": DniExtracted,
    "receta": RecetaExtracted,
    "boleta": ReciboExtracted,
}


def _strip_markdown_fences(text: str) -> str:
    t = text.strip()
    t = _CODE_FENCE_START.sub("", t)
    t = _CODE_FENCE_END.sub("", t)
    return t.strip()


def _jpeg_bytes_from_data_url(data_url: str) -> bytes:
    return base64.b64decode(strip_data_url_prefix(data_url))


class VisionService:
    def __init__(
        self,
        client: VisionCompletionClient,
        gatekeeper: GatekeeperPort,
        *,
        prompts_by_type: dict[DocumentType, str],
        settings: Settings,
    ) -> None:
        self._client = client
        self._gatekeeper = gatekeeper
        self._prompts_by_type = prompts_by_type
        self._settings = settings

    def extract_dni(self, images_base64: list[str]) -> DniExtracted:
        result = self.analyze("dni", images_base64)
        return DniExtracted.model_validate(result.draft)

    def analyze(
        self,
        document_type: DocumentType,
        images_base64: list[str],
    ) -> AnalyzeResultAccepted:
        started = time.perf_counter()
        data_urls, jpeg_bytes_list = self._preprocess_images(images_base64)

        gk_result = self._gatekeeper.evaluate(document_type, jpeg_bytes_list)
        if gk_result.decision == "reject":
            raise VisionRejectedError(
                code=gk_result.code or "wrong_document",
                message=gk_result.message or "Imagen rechazada por el gatekeeper",
            )

        system_prompt = self._prompts_by_type[document_type]
        raw_text = self._client.complete_document_extraction(
            document_type=document_type,
            system_prompt=system_prompt,
            image_data_urls=data_urls,
        )

        json_text = _strip_markdown_fences(raw_text)
        try:
            payload: dict[str, Any] = json.loads(json_text)
        except json.JSONDecodeError as exc:
            snippet = json_text[:500] + ("…" if len(json_text) > 500 else "")
            raise VisionRequestError(
                f"La respuesta del modelo no es JSON válido: {snippet}",
                status_code=502,
            ) from exc

        schema = _SCHEMA_BY_TYPE[document_type]
        try:
            parsed = schema.model_validate(payload)
        except ValidationError as exc:
            raise VisionRequestError(
                f"JSON no coincide con el esquema {document_type}: {exc!s}",
                status_code=502,
            ) from exc

        draft = parsed.model_dump()
        validation = get_validator(document_type).validate(draft)

        model_name: str | None = None
        if self._settings.llm_provider == "azure":
            model_name = self._settings.openai_vision_model

        metadata = AnalyzeMetadata(
            gatekeeper_provider=self._settings.gatekeeper_provider,
            gatekeeper_label=gk_result.label,
            gatekeeper_score=gk_result.score,
            model=model_name,
        )
        _ = time.perf_counter() - started

        return AnalyzeResultAccepted(
            document_type=document_type,
            draft=validation.draft,
            warnings=validation.warnings,
            metadata=metadata,
        )

    def _preprocess_images(
        self, images_base64: list[str]
    ) -> tuple[list[str], list[bytes]]:
        if not images_base64:
            raise VisionRequestError(
                "Se requiere al menos una imagen (images_base64 o image_base64)",
                status_code=400,
            )

        if len(images_base64) > self._settings.max_vision_input_images:
            raise VisionRequestError(
                f"Máximo {self._settings.max_vision_input_images} imágenes permitidas",
                status_code=413,
            )

        for idx, raw in enumerate(images_base64):
            stripped = raw.strip()
            if len(stripped) > self._settings.max_image_base64_chars_per_image:
                raise VisionRequestError(
                    f"Imagen {idx} supera el límite de tamaño en base64 permitido",
                    status_code=413,
                )

        data_urls: list[str] = []
        jpeg_bytes_list: list[bytes] = []
        total_jpeg = 0
        for idx, b64 in enumerate(images_base64):
            try:
                url, nbytes = preprocess_to_jpeg_data_url(
                    b64,
                    jpeg_quality=self._settings.preprocess_jpeg_quality,
                    max_width=self._settings.preprocess_max_width,
                )
            except ValueError as exc:
                raise VisionRequestError(
                    f"Imagen {idx}: {exc!s}",
                    status_code=400,
                ) from exc
            total_jpeg += nbytes
            if total_jpeg > self._settings.max_total_jpeg_bytes_after_preprocess:
                raise VisionRequestError(
                    "El tamaño total de las imágenes tras preprocesar supera el límite configurado",
                    status_code=413,
                )
            data_urls.append(url)
            jpeg_bytes_list.append(_jpeg_bytes_from_data_url(url))

        return data_urls, jpeg_bytes_list
