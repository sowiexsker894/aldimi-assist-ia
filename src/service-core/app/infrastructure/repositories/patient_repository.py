from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.entities.patient import Patient


class PatientRepository:
    """Acceso a datos para Patient (Infrastructure)."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, patient_id: int) -> Patient | None:
        return self._session.get(Patient, patient_id)

    def list_all(self) -> list[Patient]:
        stmt = select(Patient).order_by(Patient.id)
        return list(self._session.scalars(stmt).all())
