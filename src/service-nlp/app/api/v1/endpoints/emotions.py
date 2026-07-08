from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from app.api.deps import EmotionServiceDep


router = APIRouter(prefix="/emotions")


class EmotionAnalyzeRequest(BaseModel):
    text: str = Field(min_length=1, max_length=8000)
    threshold: float | None = Field(default=None, ge=0.0, le=1.0)


class EmotionItem(BaseModel):
    emotion: str
    probability: float
    percent: float
    present: bool


class EmotionAnalyzeResponse(BaseModel):
    text: str
    threshold: float
    loaded_models: int
    top_emotion: str | None
    top_probability: float | None
    risk_score: float
    alert_flag: bool
    sentiment_label: str
    emotions: list[EmotionItem]


@router.post("/analyze", response_model=EmotionAnalyzeResponse)
def analyze_emotions(
    body: EmotionAnalyzeRequest,
    svc: EmotionServiceDep,
) -> EmotionAnalyzeResponse:
    try:
        result = svc.analyze(body.text, threshold=body.threshold)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    return EmotionAnalyzeResponse(**result)