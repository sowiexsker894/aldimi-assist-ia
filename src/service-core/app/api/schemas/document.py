from datetime import datetime
from typing import Any, Literal
import uuid

from pydantic import BaseModel, Field, model_validator


DocumentType = Literal["dni", "boleta", "receta"]


class DocumentAnalyzeRequest(BaseModel):
    document_type: DocumentType
    images_base64: list[str] = Field(min_length=1)
    patient_id: int | None = Field(default=None, ge=1)

    @model_validator(mode="after")
    def validate_images_and_patient(self) -> "DocumentAnalyzeRequest":
        if not any(s and str(s).strip() for s in self.images_base64):
            raise ValueError("images_base64 debe contener al menos una imagen no vacía")
        return self


class DocumentAnalyzeResponse(BaseModel):
    analysis_session_id: str
    document_type: DocumentType
    draft: dict[str, Any]
    warnings: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class DniSaveRequest(BaseModel):
    analysis_session_id: uuid.UUID
    confirmed_fields: dict[str, Any]


class BoletaSaveRequest(BaseModel):
    analysis_session_id: uuid.UUID
    confirmed_fields: dict[str, Any]


class RecetaSaveRequest(BaseModel):
    analysis_session_id: uuid.UUID
    patient_id: int = Field(ge=1)
    confirmed_fields: dict[str, Any]


class DocumentSaveResponse(BaseModel):
    id: int
    document_type: DocumentType
    patient_id: int | None = None
    created_at: datetime
