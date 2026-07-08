from typing import Any

import httpx

from app.core.exceptions import ExternalServiceUnavailable


class NlpHttpClient:
    """Adaptador HTTP hacia service-nlp."""

    def __init__(self, base_url: str, timeout: float = 120.0) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout

    def ask_regulation(self, query: str) -> str:
        if not self._base_url:
            raise ExternalServiceUnavailable(
                "NLP_SERVICE_URL no está configurada",
                service="nlp",
            )

        payload = {
            "message": query,
            "history": [],
        }

        try:
            with httpx.Client(timeout=self._timeout) as client:
                response = client.post(
                    f"{self._base_url}/api/v1/chat",
                    json=payload,
                )
                response.raise_for_status()
        except httpx.HTTPError as exc:
            raise ExternalServiceUnavailable(
                "No se pudo consultar el chatbot de service-nlp",
                service="nlp",
            ) from exc

        data = response.json()
        return str(data.get("reply", ""))

    def analyze_emotions(self, text: str) -> dict[str, Any]:
        if not self._base_url:
            raise ExternalServiceUnavailable(
                "NLP_SERVICE_URL no está configurada",
                service="nlp",
            )

        try:
            with httpx.Client(timeout=self._timeout) as client:
                response = client.post(
                    f"{self._base_url}/api/v1/emotions/analyze",
                    json={"text": text},
                )
                response.raise_for_status()
        except httpx.HTTPError as exc:
            raise ExternalServiceUnavailable(
                "No se pudo analizar el reporte diario con service-nlp",
                service="nlp",
            ) from exc

        return response.json()
