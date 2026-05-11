class ChatService:
    """Lógica de chat: por ahora stub sin LLM."""

    def reply(self, message: str) -> str:
        text = message.strip()
        return f"[stub] Recibido: {text}"
