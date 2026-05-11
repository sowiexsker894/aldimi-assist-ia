from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.infrastructure.clients.nlp_http_client import NlpHttpClient
from app.infrastructure.clients.vision_http_client import VisionHttpClient
from app.infrastructure.persistence.session import get_db
from app.infrastructure.repositories.patient_repository import PatientRepository
from app.services.patient_service import PatientService


def get_patient_repository(
    db: Annotated[Session, Depends(get_db)],
) -> PatientRepository:
    return PatientRepository(db)


def get_nlp_http_client() -> NlpHttpClient:
    return NlpHttpClient(get_settings().nlp_service_url)


def get_vision_http_client() -> VisionHttpClient:
    return VisionHttpClient(get_settings().vision_service_url)


def get_patient_service(
    repo: Annotated[PatientRepository, Depends(get_patient_repository)],
    nlp: Annotated[NlpHttpClient, Depends(get_nlp_http_client)],
    vision: Annotated[VisionHttpClient, Depends(get_vision_http_client)],
) -> PatientService:
    return PatientService(repo, nlp, vision)
