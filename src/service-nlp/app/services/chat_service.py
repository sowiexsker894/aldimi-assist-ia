from app.infrastructure.llm.protocols import ChatMessageDict, LLMClient


class ChatService:
    def __init__(self, llm: LLMClient, *, system_prompt: str) -> None:
        self._llm = llm
        self._system_prompt = system_prompt.strip()

    def reply(
        self,
        message: str,
        *,
        history: list[ChatMessageDict] | None = None,
    ) -> str:
        msgs: list[ChatMessageDict] = []
        if self._system_prompt:
            msgs.append(ChatMessageDict(role="system", content=self._system_prompt))
        if history:
            for item in history:
                if item.get("role") == "system":
                    continue
                msgs.append(item)
        msgs.append(ChatMessageDict(role="user", content=message.strip()))
        return self._llm.complete(msgs)
