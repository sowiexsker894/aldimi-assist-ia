from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class NlpClientPort(Protocol):
    """Puerto hacia nlp-service."""

    def ask_regulation(self, query: str) -> str:
        """Envía una consulta y devuelve respuesta en texto plano."""
        ...

    def analyze_emotions(self, text: str) -> dict[str, Any]:
        """Analiza emocionalmente un texto usando service-nlp."""
        ...
