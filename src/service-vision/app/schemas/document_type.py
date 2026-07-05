from typing import Literal

DocumentType = Literal["dni", "receta", "boleta"]

GatekeeperLabel = Literal["dni", "boleta", "recibo", "ruido"]

RejectionCode = Literal[
    "blurry",
    "wrong_document",
    "unreadable",
    "too_dark",
    "unsupported_format",
    "ruido",
    "low_score",
]
