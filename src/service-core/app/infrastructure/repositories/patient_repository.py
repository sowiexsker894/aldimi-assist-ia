from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.entities.patient import Patient
from app.domain.entities.user_patient import UserPatientRow


class PatientRepository:
    """Acceso a datos para Patient (Infrastructure)."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_id(self, patient_id: int) -> Patient | None:
        return self._session.get(Patient, patient_id)

    def get_by_dni(self, dni: str) -> Patient | None:
        stmt = select(Patient).where(Patient.dni == dni)
        return self._session.scalars(stmt).first()

    def list_all(self) -> list[Patient]:
        stmt = select(Patient).order_by(Patient.id)
        return list(self._session.scalars(stmt).all())

    def add(self, patient: Patient) -> Patient:
        self._session.add(patient)
        self._session.flush()
        return patient

    def link_user_to_patient(self, user_id: int, patient_id: int) -> None:
        self._session.add(UserPatientRow(user_id=user_id, patient_id=patient_id))
        self._session.flush()

    def has_user_patient_link(self, user_id: int, patient_id: int) -> bool:
        stmt = select(UserPatientRow).where(
            UserPatientRow.user_id == user_id,
            UserPatientRow.patient_id == patient_id,
        )
        return self._session.scalars(stmt).first() is not None
