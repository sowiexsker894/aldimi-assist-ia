from typing import Annotated

from fastapi import Depends

from app.core.config import Settings, get_settings
from app.services.vision_service import VisionService

_vision_service: VisionService | None = None


def get_vision_service() -> VisionService:
    global _vision_service
    if _vision_service is None:
        _vision_service = VisionService()
    return _vision_service


SettingsDep = Annotated[Settings, Depends(get_settings)]
VisionServiceDep = Annotated[VisionService, Depends(get_vision_service)]
