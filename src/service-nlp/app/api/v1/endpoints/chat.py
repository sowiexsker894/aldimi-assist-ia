from typing import Literal

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from openai import OpenAIError

from app.api.deps import ChatServiceDep
from app.infrastructure.llm.protocols import ChatMessageDict

router = APIRouter()


class ChatMessageItem(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str = Field(min_length=1, max_length=16000)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=8000)
    history: list[ChatMessageItem] = Field(default_factory=list, max_length=40)


class ChatResponse(BaseModel):
    reply: str


@router.post(
    "/chat",
    response_model=ChatResponse,
    summary="Chat con el asistente",
    description="Reenvía el mensaje al proveedor LLM configurado (Azure OpenAI / stub).",
)
def post_chat(
    body: ChatRequest,
    svc: ChatServiceDep,
) -> ChatResponse:
    history: list[ChatMessageDict] = [
        ChatMessageDict(role=m.role, content=m.content) for m in body.history
    ]
    try:
        reply = svc.reply(body.message, history=history or None)
    except OpenAIError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
    return ChatResponse(reply=reply)
