from typing import Annotated

from fastapi import Depends

from app.core.config import Settings, get_settings
from app.core.dni_extractor_system_prompt import DNI_EXTRACTOR_SYSTEM_PROMPT
from app.infrastructure.llm.azure_vision_client import AzureVisionClient
from app.infrastructure.llm.protocols import VisionCompletionClient
from app.infrastructure.llm.stub_vision_client import StubVisionClient
from app.services.vision_service import VisionService


def _make_vision_client(settings: Settings) -> VisionCompletionClient:
    if settings.llm_provider == "stub":
        return StubVisionClient()
    return AzureVisionClient(
        base_url=settings.openai_base_url,
        api_key=settings.openai_api_key,
        model=settings.openai_vision_model,
    )


_vision_service: VisionService | None = None


def get_vision_service(
    settings: Annotated[Settings, Depends(get_settings)],
) -> VisionService:
    global _vision_service
    if _vision_service is None:
        system = (
            settings.dni_system_prompt.strip()
            if settings.dni_system_prompt.strip()
            else DNI_EXTRACTOR_SYSTEM_PROMPT
        )
        _vision_service = VisionService(
            _make_vision_client(settings),
            system_prompt=system,
            settings=settings,
        )
    return _vision_service


SettingsDep = Annotated[Settings, Depends(get_settings)]
VisionServiceDep = Annotated[VisionService, Depends(get_vision_service)]
