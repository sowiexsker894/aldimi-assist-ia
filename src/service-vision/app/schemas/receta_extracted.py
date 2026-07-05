from pydantic import BaseModel, Field


class MedicamentoItem(BaseModel):
    nombre: str
    concentracion: str | None = Field(default=None)
    forma_farmaceutica: str | None = Field(default=None)
    dosis: str | None = Field(default=None)
    frecuencia: str | None = Field(default=None)
    duracion: str | None = Field(default=None)
    cantidad: str | None = Field(default=None)


class RecetaExtracted(BaseModel):
    paciente_nombre: str | None = Field(default=None)
    paciente_edad: str | None = Field(default=None)
    medico_nombre: str | None = Field(default=None)
    medico_cmp: str | None = Field(default=None)
    institucion: str | None = Field(default=None)
    fecha_emision: str | None = Field(default=None)
    diagnostico: str | None = Field(default=None)
    medicamentos: list[MedicamentoItem] | None = Field(default=None)
    indicaciones: str | None = Field(default=None)
    observaciones: str | None = Field(default=None)
