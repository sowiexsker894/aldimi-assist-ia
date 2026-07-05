from typing import Any, Protocol


class VisionClientPort(Protocol):
    """Puerto hacia vision-service (OCR / documentos)."""

    def analyze_document(
        self,
        *,
        document_type: str,
        images_base64: list[str],
    ) -> dict[str, Any]: ...
