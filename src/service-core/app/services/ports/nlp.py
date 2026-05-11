from typing import Protocol, runtime_checkable


@runtime_checkable
class NlpClientPort(Protocol):
    """Puerto hacia nlp-service (consultas reglamento / RAG, etc.)."""

    def ask_regulation(self, query: str) -> str:
        """Envía una consulta y devuelve respuesta en texto plano."""
        ...
