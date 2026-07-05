from typing import Any, Literal

from pydantic import BaseModel, Field

from app.schemas.document_type import DocumentType, GatekeeperLabel
from app.schemas.dni_extracted import DniExtracted


class RejectionDetail(BaseModel):
    code: str
    message: str


class AnalyzeMetadata(BaseModel):
    gatekeeper_provider: str
    gatekeeper_label: GatekeeperLabel
    gatekeeper_score: float
    model: str | None = None


class AnalyzeResultAccepted(BaseModel):
    status: Literal["accepted"] = "accepted"
    document_type: DocumentType
    draft: dict[str, Any]
    warnings: list[str] = Field(default_factory=list)
    metadata: AnalyzeMetadata


class AnalyzeResultRejected(BaseModel):
    status: Literal["rejected"] = "rejected"
    rejection: RejectionDetail


AnalyzeResult = AnalyzeResultAccepted | AnalyzeResultRejected


class AnalyzeResponse(BaseModel):
    status: Literal["accepted", "rejected"]
    document_type: DocumentType | None = None
    draft: dict[str, Any] | None = None
    warnings: list[str] = Field(default_factory=list)
    metadata: AnalyzeMetadata | None = None
    rejection: RejectionDetail | None = None
    data: DniExtracted | None = Field(
        default=None,
        description="Compatibilidad legacy demo DNI",
    )
