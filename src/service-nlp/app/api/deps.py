from typing import Annotated
from app.services.emotion_service import EmotionService
from fastapi import Depends

from app.core.aldimi_system_prompt import ALDIMI_SYSTEM_PROMPT
from app.core.config import Settings, get_settings
from app.infrastructure.llm.azure_inference_client import AzureInferenceLLMClient
from app.infrastructure.llm.protocols import LLMClient
from app.infrastructure.llm.stub_llm_client import StubLLMClient
from app.services.chat_service import ChatService


def _make_llm(settings: Settings) -> LLMClient:
    if settings.llm_provider == "stub":
        return StubLLMClient()
    return AzureInferenceLLMClient(
        base_url=settings.openai_base_url,
        api_key=settings.openai_api_key,
        model=settings.openai_chat_model,
    )


_chat_service: ChatService | None = None
_emotion_service: EmotionService | None = None

def get_chat_service(settings: Annotated[Settings, Depends(get_settings)]) -> ChatService:
    global _chat_service
    if _chat_service is None:
        system = (
            #settings.chat_system_prompt.strip()
            #if settings.chat_system_prompt.strip()
            #else ALDIMI_SYSTEM_PROMPT
            ALDIMI_SYSTEM_PROMPT
        )
        _chat_service = ChatService(_make_llm(settings), system_prompt=system)
    return _chat_service

def get_emotion_service(settings: Annotated[Settings, Depends(get_settings)]) -> EmotionService:
    global _emotion_service

    if _emotion_service is None:
        try:
            _emotion_service = EmotionService(
                model_dir=settings.emotion_model_dir,
                model_prefix=settings.emotion_model_prefix,
                tokenizer_name=settings.emotion_tokenizer_name,
                threshold=settings.emotion_threshold,
                max_length=settings.emotion_max_length,
            )
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"No se pudo cargar el modelo BERT emocional: {exc}",
            ) from exc

    return _emotion_service


SettingsDep = Annotated[Settings, Depends(get_settings)]
ChatServiceDep = Annotated[ChatService, Depends(get_chat_service)]
EmotionServiceDep = Annotated[EmotionService, Depends(get_emotion_service)]