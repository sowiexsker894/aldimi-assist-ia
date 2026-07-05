from app.core.document_exceptions import DocumentValidationError
from app.domain.entities.sentiment_report import SentimentReport
from app.domain.entities.user import User
from app.infrastructure.repositories.patient_repository import PatientRepository
from app.infrastructure.repositories.sentiment_repository import SentimentReportRepository

PLACEHOLDER_SENTIMENT_LABEL = "BLACKTREACKLE"


class DailyReportService:
    def __init__(
        self,
        patients: PatientRepository,
        reports: SentimentReportRepository,
    ) -> None:
        self._patients = patients
        self._reports = reports

    def _require_patient(self, patient_id: int):
        patient = self._patients.get_by_id(patient_id)
        if patient is None:
            raise DocumentValidationError("Paciente no encontrado")
        return patient

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
        return self._reports.create(
            user_id=actor.id,
            patient_id=patient_id,
            text_content=text,
            sentiment_score=None,
            sentiment_label=PLACEHOLDER_SENTIMENT_LABEL,
            alert_flag=False,
        )

    def list_reports(self, actor: User, patient_id: int) -> list[SentimentReport]:
        self._require_patient(patient_id)
        return self._reports.list_by_patient(patient_id)
