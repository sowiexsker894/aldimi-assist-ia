from typing import Any

from app.core.document_exceptions import DocumentValidationError
from app.core.exceptions import ExternalServiceUnavailable
from app.domain.entities.sentiment_report import SentimentReport
from app.domain.entities.user import User
from app.infrastructure.repositories.patient_repository import PatientRepository
from app.infrastructure.repositories.sentiment_repository import SentimentReportRepository
from app.services.ports.nlp import NlpClientPort


FALLBACK_SENTIMENT_LABEL = "sin_analisis"


class DailyReportService:
    def __init__(
        self,
        patients: PatientRepository,
        reports: SentimentReportRepository,
        nlp: NlpClientPort,
    ) -> None:
        self._patients = patients
        self._reports = reports
        self._nlp = nlp

    def _require_patient(self, patient_id: int):
        patient = self._patients.get_by_id(patient_id)
        if patient is None:
            raise DocumentValidationError("Paciente no encontrado")
        return patient

    def _build_sentiment_details(self, analysis: dict[str, Any]) -> dict[str, Any]:
        emotions_raw = analysis.get("emotions") or []

        emotions = []
        for item in emotions_raw:
            if not isinstance(item, dict):
                continue

            emotions.append(
                {
                    "emotion": item.get("emotion"),
                    "probability": item.get("probability"),
                    "percent": item.get("percent"),
                    "present": item.get("present", False),
                }
            )

        emotions.sort(
            key=lambda item: float(item.get("probability") or 0),
            reverse=True,
        )

        return {
            "top_emotion": analysis.get("top_emotion"),
            "top_probability": analysis.get("top_probability"),
            "risk_score": analysis.get("risk_score"),
            "alert_flag": analysis.get("alert_flag", False),
            "emotions": emotions[:3],
        }

    def _analyze_sentiment(self, text: str) -> tuple[str, float | None, bool, dict[str, Any] | None]:
        try:
            analysis = self._nlp.analyze_emotions(text)
        except ExternalServiceUnavailable:
            return FALLBACK_SENTIMENT_LABEL, None, False, None

        sentiment_label = str(analysis.get("sentiment_label") or FALLBACK_SENTIMENT_LABEL)

        risk_score_raw = analysis.get("risk_score")
        sentiment_score = float(risk_score_raw) if risk_score_raw is not None else None

        alert_flag = bool(analysis.get("alert_flag", False))
        sentiment_details = self._build_sentiment_details(analysis)

        return sentiment_label, sentiment_score, alert_flag, sentiment_details

    def create_report(
        self,
        actor: User,
        patient_id: int,
        text_content: str,
    ) -> SentimentReport:
        self._require_patient(patient_id)

        text = text_content.strip()
        if not text:
            raise DocumentValidationError("El reporte no puede estar vacío")
        if len(text) > 500:
            raise DocumentValidationError("El reporte no puede superar 500 caracteres")

        sentiment_label, sentiment_score, alert_flag, sentiment_details = self._analyze_sentiment(text)

        return self._reports.create(
            user_id=actor.id,
            patient_id=patient_id,
            text_content=text,
            sentiment_score=sentiment_score,
            sentiment_label=sentiment_label,
            sentiment_details=sentiment_details,
            alert_flag=alert_flag,
        )

    def list_reports(self, actor: User, patient_id: int) -> list[SentimentReport]:
        self._require_patient(patient_id)
        return self._reports.list_by_patient(patient_id)
