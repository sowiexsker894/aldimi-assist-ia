from app.core.exceptions import ExternalServiceUnavailable


class VisionHttpClient:
    """Adaptador HTTP stub hacia vision-service (OCR, etc.)."""

    def __init__(self, base_url: str) -> None:
        self._base_url = base_url.rstrip("/")

    def extract_document_text(self, document_uri: str) -> str:
        if not self._base_url:
            raise ExternalServiceUnavailable(
                "VISION_SERVICE_URL no está configurada",
                service="vision",
            )
        raise ExternalServiceUnavailable(
            "Integración HTTP con vision-service pendiente",
            service="vision",
        )
