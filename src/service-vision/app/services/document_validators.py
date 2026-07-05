from dataclasses import dataclass
from typing import Any

from app.schemas.document_type import DocumentType
from app.services.validation_utils import (
    is_plausible_birth_date,
    is_valid_dni_number,
    is_valid_ruc,
    normalize_whitespace,
    parse_date_dd_mm_yyyy,
)


@dataclass
class ValidationResult:
    draft: dict[str, Any]
    warnings: list[str]


class DniValidator:
    def validate(self, draft: dict[str, Any]) -> ValidationResult:
        result = dict(draft)
        warnings: list[str] = []

        for key in ("nombre", "apellido_paterno", "apellido_materno", "direccion"):
            if key in result:
                result[key] = normalize_whitespace(result.get(key))

        dni = result.get("dni_number")
        if dni is not None and str(dni).strip():
            if not is_valid_dni_number(str(dni)):
                warnings.append("dni_number: debe tener 8 dígitos numéricos")
                result["dni_number"] = None

        for field in ("fecha_nacimiento", "fecha_expiracion"):
            raw = result.get(field)
            if raw is not None and str(raw).strip():
                if parse_date_dd_mm_yyyy(str(raw)) is None:
                    warnings.append(f"{field}: formato esperado DD/MM/YYYY")
                    result[field] = None
                elif field == "fecha_nacimiento" and not is_plausible_birth_date(str(raw)):
                    warnings.append(f"{field}: fecha fuera de rango plausible")
                    result[field] = None

        birth = result.get("fecha_nacimiento")
        expiry = result.get("fecha_expiracion")
        birth_date = parse_date_dd_mm_yyyy(str(birth)) if birth else None
        expiry_date = parse_date_dd_mm_yyyy(str(expiry)) if expiry else None
        if birth_date and expiry_date and expiry_date < birth_date:
            warnings.append("fecha_expiracion: anterior a fecha de nacimiento")

        has_identity = any(
            result.get(k) for k in ("dni_number", "nombre", "apellido_paterno", "apellido_materno")
        )
        if not has_identity:
            warnings.append(
                "No se extrajo información identificativa del DNI. Revise la imagen o complete manualmente."
            )

        return ValidationResult(draft=result, warnings=warnings)


class RecetaValidator:
    def validate(self, draft: dict[str, Any]) -> ValidationResult:
        result = dict(draft)
        warnings: list[str] = []

        raw_date = result.get("fecha_emision")
        if raw_date is not None and str(raw_date).strip():
            if parse_date_dd_mm_yyyy(str(raw_date)) is None:
                warnings.append("fecha_emision: formato esperado DD/MM/YYYY")
                result["fecha_emision"] = None

        cmp_val = result.get("medico_cmp")
        if cmp_val is not None and str(cmp_val).strip():
            if not str(cmp_val).strip().isdigit() or len(str(cmp_val).strip()) < 5:
                warnings.append("medico_cmp: formato de colegiatura inválido")

        meds = result.get("medicamentos")
        if not meds:
            warnings.append("medicamentos: no se detectaron ítems en la receta")

        return ValidationResult(draft=result, warnings=warnings)


class ReciboValidator:
    def validate(self, draft: dict[str, Any]) -> ValidationResult:
        result = dict(draft)
        warnings: list[str] = []

        raw_date = result.get("fecha_emision")
        if raw_date is not None and str(raw_date).strip():
            if parse_date_dd_mm_yyyy(str(raw_date)) is None:
                warnings.append("fecha_emision: formato esperado DD/MM/YYYY")
                result["fecha_emision"] = None

        ruc = result.get("emisor_ruc")
        if ruc is not None and str(ruc).strip() and not is_valid_ruc(str(ruc)):
            warnings.append("emisor_ruc: debe tener 11 dígitos")
            result["emisor_ruc"] = None

        total = result.get("total")
        if total is not None and str(total).strip():
            try:
                if float(str(total).replace(",", ".")) <= 0:
                    warnings.append("total: debe ser mayor a cero")
            except ValueError:
                warnings.append("total: formato numérico inválido")

        return ValidationResult(draft=result, warnings=warnings)


def get_validator(document_type: DocumentType) -> DniValidator | RecetaValidator | ReciboValidator:
    if document_type == "dni":
        return DniValidator()
    if document_type == "receta":
        return RecetaValidator()
    return ReciboValidator()
