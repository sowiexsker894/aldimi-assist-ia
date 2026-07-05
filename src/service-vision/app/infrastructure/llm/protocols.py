from typing import Protocol

from app.schemas.document_type import DocumentType


class VisionCompletionClient(Protocol):
    def complete_document_extraction(
        self,
        *,
        document_type: DocumentType,
        system_prompt: str,
        image_data_urls: list[str],
    ) -> str: ...
