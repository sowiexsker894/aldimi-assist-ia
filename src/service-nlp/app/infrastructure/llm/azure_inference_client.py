from openai import OpenAI

from app.infrastructure.llm.protocols import ChatMessageDict


class AzureInferenceLLMClient:
    """Cliente OpenAI-compatible (Azure /openai/v1 del portal)."""

    def __init__(
        self, *, base_url: str, api_key: str, model: str, timeout_seconds: float = 120.0
    ) -> None:
        self._model = model
        self._client = OpenAI(
            base_url=base_url,
            api_key=api_key,
            timeout=timeout_seconds,
        )

    def complete(self, messages: list[ChatMessageDict]) -> str:
        completion = self._client.chat.completions.create(
            model=self._model,
            messages=messages,
        )
        choice = completion.choices[0].message
        content = choice.content
        if content is None:
            return ""
        return content
