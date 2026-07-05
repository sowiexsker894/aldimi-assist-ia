from typing import Any

from app.core.document_exceptions import DocumentValidationError
from app.domain.entities.patient import Patient
from app.infrastructure.repositories.patient_repository import PatientRepository
from app.services.ports.nlp import NlpClientPort
from app.services.ports.vision import VisionClientPort

_PATIENT_FIELDS = (
    "dni",
    "primer_apellido",
    "segundo_apellido",
    "primer_nombre",
    "segundo_nombre",
    "sexo",
    "fecha_nacimiento",
    "nacionalidad",
    "estado_civil",
    "direccion",
    "ubigeo",
)


class PatientService:
    """Capa de aplicación: orquesta repositorios y puertos externos."""

    def __init__(
        self,
        patient_repo: PatientRepository,
        nlp_client: NlpClientPort,
        vision_client: VisionClientPort,
    ) -> None:
        self._patient_repo = patient_repo
        self._nlp_client = nlp_client
        self._vision_client = vision_client

    def list_patients(self) -> list[Patient]:
        return self._patient_repo.list_all()

    def get_patient(self, patient_id: int) -> Patient | None:
        return self._patient_repo.get_by_id(patient_id)

    def create_patient(self, *, full_name: str, **fields: Any) -> Patient:
        """Registro manual de paciente. DNI (si se envía) debe ser único."""
        dni = fields.get("dni")
        if dni and self._patient_repo.get_by_dni(dni) is not None:
            raise DocumentValidationError("Ya existe un paciente con ese DNI")
        data = {key: fields.get(key) for key in _PATIENT_FIELDS}
        return self._patient_repo.add(Patient(full_name=full_name.strip(), **data))
