from app.infrastructure.gatekeeper.protocols import GatekeeperResult
from app.schemas.document_type import DocumentType, GatekeeperLabel


def document_type_to_stub_label(document_type: DocumentType) -> GatekeeperLabel:
    """Mapeo provisional hasta que el clasificador ML esté entrenado."""
    if document_type == "dni":
        return "dni"
    if document_type == "boleta":
        return "boleta"
    # receta: sin etiqueta en el modelo; placeholder coherente con stub
    return "recibo"


class StubGatekeeper:
    """Siempre acepta; devuelve label mapeada y score=1.0."""

    def evaluate(
        self,
        document_type: DocumentType,
        images_jpeg: list[bytes],
    ) -> GatekeeperResult:
        _ = images_jpeg
        return GatekeeperResult(
            decision="accept",
            label=document_type_to_stub_label(document_type),
            score=1.0,
        )
