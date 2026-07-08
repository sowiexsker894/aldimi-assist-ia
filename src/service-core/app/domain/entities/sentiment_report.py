from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, JSON, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.domain.base import Base


class SentimentReport(Base):
    """Reporte de análisis de sentimiento generado por service-nlp."""

    __tablename__ = "sentiment_reports"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    patient_id: Mapped[int | None] = mapped_column(
        ForeignKey("patients.id", ondelete="SET NULL"),
        nullable=True,
    )
    text_content: Mapped[str] = mapped_column(Text(), nullable=False)
    sentiment_score: Mapped[float | None] = mapped_column(Float(), nullable=True)
    sentiment_label: Mapped[str | None] = mapped_column(String(16), nullable=True)
    sentiment_details: Mapped[dict | None] = mapped_column(JSON(), nullable=True)
    alert_flag: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
