from app.core.exceptions import ExternalServiceUnavailable


class NlpHttpClient:
    """Adaptador HTTP stub hacia nlp-service (sustituir por llamadas reales con httpx)."""

    def __init__(self, base_url: str) -> None:
        self._base_url = base_url.rstrip("/")

    def ask_regulation(self, query: str) -> str:
        if not self._base_url:
            raise ExternalServiceUnavailable(
                "NLP_SERVICE_URL no está configurada",
                service="nlp",
            )
        raise ExternalServiceUnavailable(
            "Integración HTTP con nlp-service pendiente",
            service="nlp",
        )
