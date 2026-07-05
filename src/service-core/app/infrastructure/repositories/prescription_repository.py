from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.entities.prescription import Prescription


class PrescriptionRepository:
    """Acceso a datos para Prescription (Infrastructure)."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def create(
        self,
        *,
        patient_id: int | None,
        document_id: int | None,
        medico: str | None,
        cedula_medico: str | None,
        paciente_nombre: str | None,
        medicamentos: list,
        indicaciones: str | None,
        nombre_clinica: str | None,
        fecha: date | None,
        created_by: int | None,
    ) -> Prescription:
        row = Prescription(
            patient_id=patient_id,
            document_id=document_id,
            medico=medico,
            cedula_medico=cedula_medico,
            paciente_nombre=paciente_nombre,
            medicamentos=medicamentos,
            indicaciones=indicaciones,
            nombre_clinica=nombre_clinica,
            fecha=fecha,
            created_by=created_by,
        )
        self._session.add(row)
        self._session.flush()
        return row

    def list_by_patient(self, patient_id: int) -> list[Prescription]:
        stmt = (
            select(Prescription)
            .where(Prescription.patient_id == patient_id)
            .order_by(Prescription.created_at.desc())
        )
        return list(self._session.scalars(stmt).all())
