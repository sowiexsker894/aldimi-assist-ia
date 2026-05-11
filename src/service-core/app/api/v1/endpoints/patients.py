from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_current_user, get_patient_service
from app.api.schemas.patient import PatientRead
from app.domain.entities.user import User
from app.services.patient_service import PatientService

router = APIRouter()


@router.get("/", response_model=list[PatientRead])
def list_patients(
    _: Annotated[User, Depends(get_current_user)],
    svc: Annotated[PatientService, Depends(get_patient_service)],
) -> list[PatientRead]:
    return svc.list_patients()


@router.get("/{patient_id}", response_model=PatientRead)
def get_patient(
    patient_id: int,
    _auth: Annotated[User, Depends(get_current_user)],
    svc: Annotated[PatientService, Depends(get_patient_service)],
) -> PatientRead:
    patient = svc.get_patient(patient_id)
    if patient is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paciente no encontrado",
        )
    return patient
