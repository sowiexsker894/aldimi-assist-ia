from pydantic import BaseModel, Field


class DniExtracted(BaseModel):
    nombre: str | None = Field(default=None)
    apellido_paterno: str | None = Field(default=None)
    apellido_materno: str | None = Field(default=None)
    dni_number: str | None = Field(default=None)
    sexo: str | None = Field(default=None)
    nacionalidad: str | None = Field(default=None)
    fecha_nacimiento: str | None = Field(default=None)
    fecha_expiracion: str | None = Field(default=None)
    lugar_nacimiento: str | None = Field(default=None)
    direccion: str | None = Field(default=None)
