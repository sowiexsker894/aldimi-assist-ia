from dataclasses import dataclass
from typing import Literal, Protocol

from app.schemas.document_type import DocumentType, GatekeeperLabel, RejectionCode


@dataclass(frozen=True)
class GatekeeperResult:
    decision: Literal["accept", "reject"]
    label: GatekeeperLabel
    score: float
    code: RejectionCode | None = None
    message: str | None = None


class GatekeeperPort(Protocol):
    def evaluate(
        self,
        document_type: DocumentType,
        images_jpeg: list[bytes],
    ) -> GatekeeperResult: ...
