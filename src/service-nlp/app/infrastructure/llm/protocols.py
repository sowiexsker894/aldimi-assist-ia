from typing import Protocol, TypedDict


class ChatMessageDict(TypedDict):
    role: str
    content: str


class LLMClient(Protocol):
    def complete(self, messages: list[ChatMessageDict]) -> str: ...
