from typing import Protocol


class VisionCompletionClient(Protocol):
    def complete_dni_extraction(
        self, *, system_prompt: str, image_data_urls: list[str]
    ) -> str: ...
