from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class DailyReportCreate(BaseModel):
    text_content: str = Field(min_length=1, max_length=500)


class DailyReportRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int | None = None
    patient_id: int | None = None
    text_content: str
    sentiment_label: str | None = None
    sentiment_score: float | None = None
    sentiment_details: dict[str, Any] | None = None
    alert_flag: bool
    created_at: datetime
