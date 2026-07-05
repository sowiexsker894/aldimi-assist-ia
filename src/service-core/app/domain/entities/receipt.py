from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Date, DateTime, ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.domain.base import Base


class Receipt(Base):
    """Boleta/comprobante normalizado y consultable (complementa documents)."""

    __tablename__ = "receipts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    patient_id: Mapped[int | None] = mapped_column(
        ForeignKey("patients.id", ondelete="SET NULL"),
        nullable=True,
    )
    document_id: Mapped[int | None] = mapped_column(
        ForeignKey("documents.id", ondelete="SET NULL"),
        nullable=True,
    )
    monto_recibido: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    nombre: Mapped[str | None] = mapped_column(String(255), nullable=True)
    fecha: Mapped[date | None] = mapped_column(Date(), nullable=True)
    medio_pago: Mapped[str | None] = mapped_column(String(64), nullable=True)
    numero_operacion: Mapped[str | None] = mapped_column(String(64), nullable=True)
    created_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
