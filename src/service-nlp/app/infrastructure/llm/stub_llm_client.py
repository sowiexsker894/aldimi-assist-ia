from app.infrastructure.llm.protocols import ChatMessageDict


class StubLLMClient:
    """Desarrollo sin credenciales Azure."""

    def complete(self, messages: list[ChatMessageDict]) -> str:
        last = messages[-1] if messages else {"role": "user", "content": ""}
        text = str(last.get("content", "")).strip()
        return f"[stub] Recibido: {text}"
