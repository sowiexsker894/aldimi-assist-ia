import json

from openai import OpenAI

from app.infrastructure.llm.protocols import VisionCompletionClient
from app.schemas.document_type import DocumentType


_USER_MESSAGES: dict[DocumentType, str] = {
    "dni": (
        "Analiza estas imágenes del documento de identidad peruano "
        "y devuelve solo el JSON indicado en las reglas."
    ),
    "receta": (
        "Analiza estas imágenes de la receta médica "
        "y devuelve solo el JSON indicado en las reglas."
    ),
    "boleta": (
        "Analiza estas imágenes del comprobante de pago (boleta o recibo) "
        "y devuelve solo el JSON indicado en las reglas."
    ),
}


class AzureVisionClient:
    """Chat completions multimodal (Azure /openai/v1)."""

    def __init__(
        self, *, base_url: str, api_key: str, model: str, timeout_seconds: float = 120.0
    ) -> None:
        self._model = model
        self._client = OpenAI(
            base_url=base_url,
            api_key=api_key,
            timeout=timeout_seconds,
        )

    def complete_document_extraction(
        self,
        *,
        document_type: DocumentType,
        system_prompt: str,
        image_data_urls: list[str],
    ) -> str:
        user_content: list[object] = [
            {"type": "text", "text": _USER_MESSAGES[document_type]}
        ]
        for url in image_data_urls:
            user_content.append(
                {"type": "image_url", "image_url": {"url": url}}
            )

        completion = self._client.chat.completions.create(
            model=self._model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content},
            ],
        )
        choice = completion.choices[0].message
        text = choice.content
        return text or ""
