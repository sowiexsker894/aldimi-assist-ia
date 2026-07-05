from datetime import date
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.entities.receipt import Receipt


class ReceiptRepository:
    """Acceso a datos para Receipt (Infrastructure)."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def create(
        self,
        *,
        patient_id: int | None,
        document_id: int | None,
        monto_recibido: Decimal | None,
        nombre: str | None,
        fecha: date | None,
        medio_pago: str | None,
        numero_operacion: str | None,
        created_by: int | None,
    ) -> Receipt:
        row = Receipt(
            patient_id=patient_id,
            document_id=document_id,
            monto_recibido=monto_recibido,
            nombre=nombre,
            fecha=fecha,
            medio_pago=medio_pago,
            numero_operacion=numero_operacion,
            created_by=created_by,
        )
        self._session.add(row)
        self._session.flush()
        return row

    def list_by_patient(self, patient_id: int) -> list[Receipt]:
        stmt = (
            select(Receipt)
            .where(Receipt.patient_id == patient_id)
            .order_by(Receipt.created_at.desc())
        )
        return list(self._session.scalars(stmt).all())
