from app.domain.entities.patient import Patient
from app.infrastructure.repositories.patient_repository import PatientRepository
from app.services.ports.nlp import NlpClientPort
from app.services.ports.vision import VisionClientPort


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
