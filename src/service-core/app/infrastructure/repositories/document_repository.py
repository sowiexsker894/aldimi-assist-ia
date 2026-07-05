from datetime import datetime, timezone
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.entities.document import AnalysisSession, Document


class AnalysisSessionRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(
        self,
        *,
        user_id: int,
        patient_id: int | None,
        document_type: str,
        draft: dict,
        warnings: list[str],
        gatekeeper_label: str | None,
        gatekeeper_score: float | None,
        expires_at: datetime,
    ) -> AnalysisSession:
        row = AnalysisSession(
            id=uuid.uuid4(),
            user_id=user_id,
            patient_id=patient_id,
            document_type=document_type,
            draft=draft,
            warnings=warnings,
            gatekeeper_label=gatekeeper_label,
            gatekeeper_score=gatekeeper_score,
            expires_at=expires_at,
            consumed=False,
        )
        self._session.add(row)
        self._session.flush()
        return row

    def get_by_id(self, session_id: uuid.UUID) -> AnalysisSession | None:
        return self._session.get(AnalysisSession, session_id)

    def mark_consumed(self, session: AnalysisSession) -> None:
        session.consumed = True
        self._session.flush()


class DocumentRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(
        self,
        *,
        patient_id: int | None,
        document_type: str,
        confirmed_fields: dict,
        created_by: int,
        analysis_session_id: uuid.UUID | None,
    ) -> Document:
        row = Document(
            patient_id=patient_id,
            document_type=document_type,
            confirmed_fields=confirmed_fields,
            created_by=created_by,
            analysis_session_id=analysis_session_id,
        )
        self._session.add(row)
        self._session.flush()
        return row

    def list_by_patient(self, patient_id: int) -> list[Document]:
        stmt = (
            select(Document)
            .where(Document.patient_id == patient_id)
            .order_by(Document.created_at.desc())
        )
        return list(self._session.scalars(stmt).all())
