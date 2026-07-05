from typing import Any

import httpx

from app.core.exceptions import ExternalServiceUnavailable


class VisionHttpClient:
    """Cliente HTTP hacia service-vision."""

    def __init__(self, base_url: str, *, timeout_seconds: float = 120.0) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout_seconds

    def ping(self) -> dict[str, str]:
        if not self._base_url:
            raise ExternalServiceUnavailable(
                "VISION_SERVICE_URL no está configurada",
                service="vision",
            )
        url = f"{self._base_url}/api/v1/health"
        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.get(url)
                response.raise_for_status()
        except httpx.HTTPError as exc:
            raise ExternalServiceUnavailable(
                f"Error de conexión con vision-service: {exc!s}",
                service="vision",
            ) from exc
        data = response.json()
        return data if isinstance(data, dict) else {"status": "ok"}

    def analyze_document(
        self,
        *,
        document_type: str,
        images_base64: list[str],
    ) -> dict[str, Any]:
        if not self._base_url:
            raise ExternalServiceUnavailable(
                "VISION_SERVICE_URL no está configurada",
                service="vision",
            )

        url = f"{self._base_url}/api/v1/analyze"
        payload = {
            "document_type": document_type,
            "images_base64": images_base64,
        }
        try:
            with httpx.Client(timeout=self._timeout) as client:
                response = client.post(url, json=payload)
        except httpx.HTTPError as exc:
            raise ExternalServiceUnavailable(
                f"Error de conexión con vision-service: {exc!s}",
                service="vision",
            ) from exc

        if response.status_code == 422:
            body = response.json()
            detail = body.get("detail", body) if isinstance(body, dict) else body
            if isinstance(detail, dict) and detail.get("status") == "rejected":
                return detail
            if isinstance(detail, dict) and "rejection" in detail:
                return {"status": "rejected", **detail}
            return {
                "status": "rejected",
                "rejection": {
                    "code": "wrong_document",
                    "message": str(detail),
                },
            }

        if response.status_code >= 400:
            try:
                body = response.json()
                detail = body.get("detail", body) if isinstance(body, dict) else response.text
            except ValueError:
                detail = response.text
            raise ExternalServiceUnavailable(
                f"vision-service respondió {response.status_code}: {detail}",
                service="vision",
            )

        data = response.json()
        if not isinstance(data, dict):
            raise ExternalServiceUnavailable(
                "Respuesta inválida de vision-service",
                service="vision",
            )
        return data
