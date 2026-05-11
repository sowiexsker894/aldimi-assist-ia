from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.api.deps import ChatServiceDep

router = APIRouter()


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=8000)


class ChatResponse(BaseModel):
    reply: str


@router.post(
    "/chat",
    response_model=ChatResponse,
    summary="Chat (stub)",
    description="Respuesta de ejemplo hasta integrar el modelo / orquestación.",
)
def post_chat(
    body: ChatRequest,
    svc: ChatServiceDep,
) -> ChatResponse:
    return ChatResponse(reply=svc.reply(body.message))
