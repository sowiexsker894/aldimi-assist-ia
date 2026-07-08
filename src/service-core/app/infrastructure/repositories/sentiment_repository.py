from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.entities.sentiment_report import SentimentReport


class SentimentReportRepository:
    """Acceso a datos para SentimentReport (Infrastructure)."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def create(
        self,
        *,
        user_id: int | None,
        patient_id: int | None,
        text_content: str,
        sentiment_score: float | None,
        sentiment_label: str | None,
        sentiment_details: dict | None = None,
        alert_flag: bool = False,
    ) -> SentimentReport:
        row = SentimentReport(
            user_id=user_id,
            patient_id=patient_id,
            text_content=text_content,
            sentiment_score=sentiment_score,
            sentiment_label=sentiment_label,
            sentiment_details=sentiment_details,
            alert_flag=alert_flag,
        )
        self._session.add(row)
        self._session.flush()
        return row

    def list_by_patient(self, patient_id: int) -> list[SentimentReport]:
        stmt = (
            select(SentimentReport)
            .where(SentimentReport.patient_id == patient_id)
            .order_by(SentimentReport.created_at.desc())
        )
        return list(self._session.scalars(stmt).all())
