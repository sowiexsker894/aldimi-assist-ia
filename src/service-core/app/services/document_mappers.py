"""Mapeo de campos OCR (confirmed_fields JSONB) a columnas normalizadas.

Resuelve el desajuste de nombres entre el schema OCR de service-vision
(nombre, apellido_paterno, ...) y el contrato de datos en db_update.md.
"""

from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from typing import Any


def _clean_str(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def parse_date(value: Any) -> date | None:
    """Acepta DD/MM/YYYY, DD-MM-YYYY o ISO (YYYY-MM-DD)."""
    text = _clean_str(value)
    if text is None:
        return None
    for fmt in ("%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(text, fmt).date()
        except ValueError:
            continue
    return None


def parse_decimal(value: Any) -> Decimal | None:
    text = _clean_str(value)
    if text is None:
        return None
    text = text.replace(",", "").replace("S/", "").replace("s/", "").strip()
    try:
        return Decimal(text)
    except (InvalidOperation, ValueError):
        return None


def patient_fields_from_dni(fields: dict[str, Any]) -> dict[str, Any]:
    """Columnas normalizadas de patients a partir del draft/confirmed DNI."""
    return {
        "dni": _clean_str(fields.get("dni_number") or fields.get("dni")),
        "primer_apellido": _clean_str(
            fields.get("apellido_paterno") or fields.get("primer_apellido")
        ),
        "segundo_apellido": _clean_str(
            fields.get("apellido_materno") or fields.get("segundo_apellido")
        ),
        "primer_nombre": _clean_str(fields.get("nombre") or fields.get("primer_nombre")),
        "segundo_nombre": _clean_str(fields.get("segundo_nombre")),
        "sexo": _clean_str(fields.get("sexo")),
        "fecha_nacimiento": parse_date(fields.get("fecha_nacimiento")),
        "nacionalidad": _clean_str(fields.get("nacionalidad")),
        "estado_civil": _clean_str(fields.get("estado_civil")),
        "direccion": _clean_str(fields.get("direccion")),
        "ubigeo": _clean_str(fields.get("ubigeo")),
    }


def full_name_from_dni(fields: dict[str, Any]) -> str:
    parts = [
        fields.get("nombre") or fields.get("primer_nombre"),
        fields.get("apellido_paterno") or fields.get("primer_apellido"),
        fields.get("apellido_materno") or fields.get("segundo_apellido"),
    ]
    joined = " ".join(str(p).strip() for p in parts if p and str(p).strip())
    return joined or "Paciente sin nombre"


def prescription_fields_from_receta(fields: dict[str, Any]) -> dict[str, Any]:
    medicamentos = fields.get("medicamentos")
    if isinstance(medicamentos, list):
        meds = medicamentos
    elif medicamentos is None or (isinstance(medicamentos, str) and not medicamentos.strip()):
        meds = []
    else:
        meds = [medicamentos]
    return {
        "medico": _clean_str(fields.get("medico")),
        "cedula_medico": _clean_str(fields.get("cedula_medico")),
        "paciente_nombre": _clean_str(fields.get("paciente_nombre") or fields.get("paciente")),
        "medicamentos": meds,
        "indicaciones": _clean_str(fields.get("indicaciones")),
        "nombre_clinica": _clean_str(fields.get("nombre_clinica") or fields.get("clinica")),
        "fecha": parse_date(fields.get("fecha")),
    }


def receipt_fields_from_boleta(fields: dict[str, Any]) -> dict[str, Any]:
    return {
        "monto_recibido": parse_decimal(fields.get("monto_recibido") or fields.get("total")),
        "nombre": _clean_str(fields.get("nombre")),
        "fecha": parse_date(fields.get("fecha") or fields.get("fecha_emision")),
        "medio_pago": _clean_str(fields.get("medio_pago")),
        "numero_operacion": _clean_str(
            fields.get("numero_operacion") or fields.get("nro_operacion")
        ),
    }
