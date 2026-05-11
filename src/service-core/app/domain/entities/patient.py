from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.domain.base import Base


class Patient(Base):
    """Ejemplo de entidad de dominio (albergado / paciente) — scaffold."""

    __tablename__ = "patients"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
