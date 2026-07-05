import json

from app.infrastructure.llm.protocols import VisionCompletionClient
from app.schemas.document_type import DocumentType
from app.schemas.dni_extracted import DniExtracted
from app.schemas.receta_extracted import RecetaExtracted
from app.schemas.recibo_extracted import ReciboExtracted


def _empty_payload(document_type: DocumentType) -> dict[str, object]:
    if document_type == "dni":
        return DniExtracted().model_dump()
    if document_type == "receta":
        return RecetaExtracted().model_dump()
    return ReciboExtracted().model_dump()


class StubVisionClient:
    """Respuesta JSON mínima válida sin llamar a Azure."""

    def complete_document_extraction(
        self,
        *,
        document_type: DocumentType,
        system_prompt: str,
        image_data_urls: list[str],
    ) -> str:
        _ = system_prompt, image_data_urls
        return json.dumps(_empty_payload(document_type), ensure_ascii=False)
