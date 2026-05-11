from typing import Annotated

from fastapi import Depends

from app.core.config import Settings, get_settings
from app.services.chat_service import ChatService

_chat_service: ChatService | None = None


def get_chat_service() -> ChatService:
    global _chat_service
    if _chat_service is None:
        _chat_service = ChatService()
    return _chat_service


SettingsDep = Annotated[Settings, Depends(get_settings)]
ChatServiceDep = Annotated[ChatService, Depends(get_chat_service)]
