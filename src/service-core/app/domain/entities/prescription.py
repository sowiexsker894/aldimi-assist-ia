from datetime import date, datetime

from sqlalchemy import Date, DateTime, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.domain.base import Base


class Prescription(Base):
    """Receta médica normalizada y consultable (complementa documents)."""

    __tablename__ = "prescriptions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    patient_id: Mapped[int | None] = mapped_column(
        ForeignKey("patients.id", ondelete="SET NULL"),
        nullable=True,
    )
    document_id: Mapped[int | None] = mapped_column(
        ForeignKey("documents.id", ondelete="SET NULL"),
        nullable=True,
    )
    medico: Mapped[str | None] = mapped_column(String(255), nullable=True)
    cedula_medico: Mapped[str | None] = mapped_column(String(64), nullable=True)
    paciente_nombre: Mapped[str | None] = mapped_column(String(255), nullable=True)
    medicamentos: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    indicaciones: Mapped[str | None] = mapped_column(Text(), nullable=True)
    nombre_clinica: Mapped[str | None] = mapped_column(String(255), nullable=True)
    fecha: Mapped[date | None] = mapped_column(Date(), nullable=True)
    created_by: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
