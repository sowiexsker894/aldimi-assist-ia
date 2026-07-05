from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class PatientCreate(BaseModel):
    full_name: str = Field(min_length=1, max_length=255)
    dni: str | None = Field(default=None, min_length=8, max_length=8)
    primer_apellido: str | None = Field(default=None, max_length=120)
    segundo_apellido: str | None = Field(default=None, max_length=120)
    primer_nombre: str | None = Field(default=None, max_length=120)
    segundo_nombre: str | None = Field(default=None, max_length=120)
    sexo: str | None = Field(default=None, max_length=16)
    fecha_nacimiento: date | None = None
    nacionalidad: str | None = Field(default=None, max_length=64)
    estado_civil: str | None = Field(default=None, max_length=32)
    direccion: str | None = Field(default=None, max_length=512)
    ubigeo: str | None = Field(default=None, max_length=6)


class PatientRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    dni: str | None = None
    primer_apellido: str | None = None
    segundo_apellido: str | None = None
    primer_nombre: str | None = None
    segundo_nombre: str | None = None
    sexo: str | None = None
    fecha_nacimiento: date | None = None
    nacionalidad: str | None = None
    estado_civil: str | None = None
    direccion: str | None = None
    ubigeo: str | None = None
    created_at: datetime
