import json
import re

from pydantic import ValidationError

from app.core.config import Settings
from app.infrastructure.image_preprocess import preprocess_to_jpeg_data_url
from app.infrastructure.llm.protocols import VisionCompletionClient
from app.schemas.dni_extracted import DniExtracted
from app.services.vision_exceptions import VisionRequestError


_CODE_FENCE_START = re.compile(r"^\s*```(?:json)?\s*", re.IGNORECASE)
_CODE_FENCE_END = re.compile(r"\s*```\s*$")


def _strip_markdown_fences(text: str) -> str:
    t = text.strip()
    t = _CODE_FENCE_START.sub("", t)
    t = _CODE_FENCE_END.sub("", t)
    return t.strip()


class VisionService:
    def __init__(
        self,
        client: VisionCompletionClient,
        *,
        system_prompt: str,
        settings: Settings,
    ) -> None:
        self._client = client
        self._system_prompt = system_prompt.strip()
        self._settings = settings

    def extract_dni(self, images_base64: list[str]) -> DniExtracted:
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

        raw_text = self._client.complete_dni_extraction(
            system_prompt=self._system_prompt,
            image_data_urls=data_urls,
        )

        json_text = _strip_markdown_fences(raw_text)
        try:
            payload = json.loads(json_text)
        except json.JSONDecodeError as exc:
            snippet = json_text[:500] + ("…" if len(json_text) > 500 else "")
            raise VisionRequestError(
                f"La respuesta del modelo no es JSON válido: {snippet}",
                status_code=502,
            ) from exc

        try:
            return DniExtracted.model_validate(payload)
        except ValidationError as exc:
            raise VisionRequestError(
                f"JSON no coincide con el esquema DNI: {exc!s}",
                status_code=502,
            ) from exc
