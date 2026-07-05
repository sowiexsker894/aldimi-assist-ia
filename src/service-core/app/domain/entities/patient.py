from datetime import date, datetime

from sqlalchemy import Date, DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.domain.base import Base


class Patient(Base):
    """Entidad de dominio: albergado / paciente atendido por ALDIMI."""

    __tablename__ = "patients"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    dni: Mapped[str | None] = mapped_column(String(8), unique=True, nullable=True)
    primer_apellido: Mapped[str | None] = mapped_column(String(120), nullable=True)
    segundo_apellido: Mapped[str | None] = mapped_column(String(120), nullable=True)
    primer_nombre: Mapped[str | None] = mapped_column(String(120), nullable=True)
    segundo_nombre: Mapped[str | None] = mapped_column(String(120), nullable=True)
    sexo: Mapped[str | None] = mapped_column(String(16), nullable=True)
    fecha_nacimiento: Mapped[date | None] = mapped_column(Date(), nullable=True)
    nacionalidad: Mapped[str | None] = mapped_column(String(64), nullable=True)
    estado_civil: Mapped[str | None] = mapped_column(String(32), nullable=True)
    direccion: Mapped[str | None] = mapped_column(String(512), nullable=True)
    ubigeo: Mapped[str | None] = mapped_column(String(6), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
