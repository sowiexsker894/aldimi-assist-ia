import pytest

from app.infrastructure.gatekeeper.stub_gatekeeper import StubGatekeeper
from app.services.document_validators import DniValidator


def test_stub_gatekeeper_always_accepts_dni() -> None:
    gk = StubGatekeeper()
    result = gk.evaluate("dni", [b"fake-jpeg"])
    assert result.decision == "accept"
    assert result.label == "dni"
    assert result.score == 1.0


def test_stub_gatekeeper_maps_boleta_to_boleta() -> None:
    gk = StubGatekeeper()
    result = gk.evaluate("boleta", [b"fake-jpeg"])
    assert result.decision == "accept"
    assert result.label == "boleta"


def test_dni_validator_invalid_number_warning() -> None:
    validator = DniValidator()
    out = validator.validate({"dni_number": "1234", "nombre": "JUAN"})
    assert out.draft["dni_number"] is None
    assert any("dni_number" in w for w in out.warnings)
