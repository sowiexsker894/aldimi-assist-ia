from typing import Protocol, runtime_checkable


@runtime_checkable
class VisionClientPort(Protocol):
    """Puerto hacia vision-service (OCR / documentos)."""

    def extract_document_text(self, document_uri: str) -> str:
        """Solicita extracción de texto a partir de un documento (URI o referencia)."""
        ...
