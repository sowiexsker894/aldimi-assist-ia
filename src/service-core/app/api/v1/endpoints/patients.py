from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import (
    get_current_user,
    get_daily_report_service,
    get_patient_family_service,
    get_patient_service,
)
from app.api.schemas.daily_report import DailyReportCreate, DailyReportRead
from app.api.schemas.family_member import FamilyMemberCreate, FamilyMemberRead
from app.api.schemas.patient import PatientCreate, PatientRead
from app.core.document_exceptions import DocumentValidationError
from app.domain.enums import UserRole
from app.domain.entities.user import User
from app.services.patient_service import PatientService
from app.services.daily_report_service import DailyReportService
from app.services.patient_family_service import PatientFamilyService

router = APIRouter()

_STAFF_ROLES = {UserRole.ADMIN.value, UserRole.VOLUNTEER.value}


@router.get("/", response_model=list[PatientRead])
def list_patients(
    _: Annotated[User, Depends(get_current_user)],
    svc: Annotated[PatientService, Depends(get_patient_service)],
) -> list[PatientRead]:
    return svc.list_patients()


@router.post(
    "/",
    response_model=PatientRead,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar paciente (ADMIN o VOLUNTEER)",
)
def create_patient(
    body: PatientCreate,
    user: Annotated[User, Depends(get_current_user)],
    svc: Annotated[PatientService, Depends(get_patient_service)],
) -> PatientRead:
    roles = {r.role for r in user.roles}
    if not (roles & _STAFF_ROLES):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requiere rol de administrador o voluntario",
        )
    try:
        return svc.create_patient(**body.model_dump())
    except DocumentValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc


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


@router.get("/{patient_id}/daily-reports", response_model=list[DailyReportRead])
def list_daily_reports(
    patient_id: int,
    user: Annotated[User, Depends(get_current_user)],
    svc: Annotated[DailyReportService, Depends(get_daily_report_service)],
) -> list[DailyReportRead]:
    roles = {r.role for r in user.roles}
    if not (roles & _STAFF_ROLES):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requiere rol de administrador o voluntario",
        )
    try:
        return svc.list_reports(user, patient_id)
    except DocumentValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@router.post(
    "/{patient_id}/daily-reports",
    response_model=DailyReportRead,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar reporte diario corto (ADMIN o VOLUNTEER)",
)
def create_daily_report(
    patient_id: int,
    body: DailyReportCreate,
    user: Annotated[User, Depends(get_current_user)],
    svc: Annotated[DailyReportService, Depends(get_daily_report_service)],
) -> DailyReportRead:
    roles = {r.role for r in user.roles}
    if not (roles & _STAFF_ROLES):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requiere rol de administrador o voluntario",
        )
    try:
        return svc.create_report(user, patient_id, body.text_content)
    except DocumentValidationError as exc:
        detail = str(exc)
        code = (
            status.HTTP_404_NOT_FOUND
            if detail == "Paciente no encontrado"
            else status.HTTP_400_BAD_REQUEST
        )
        raise HTTPException(status_code=code, detail=detail) from exc


def _family_read(user: User) -> FamilyMemberRead:
    return FamilyMemberRead(
        id=user.id,
        full_name=user.full_name,
        document_number=user.document_number,
        phone=user.phone,
        email=user.email,
    )


@router.get("/{patient_id}/family-members", response_model=list[FamilyMemberRead])
def list_family_members(
    patient_id: int,
    user: Annotated[User, Depends(get_current_user)],
    svc: Annotated[PatientFamilyService, Depends(get_patient_family_service)],
) -> list[FamilyMemberRead]:
    roles = {r.role for r in user.roles}
    if not (roles & _STAFF_ROLES):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requiere rol de administrador o voluntario",
        )
    try:
        members = svc.list_family_members(user, patient_id)
    except DocumentValidationError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc
    return [_family_read(m) for m in members]


@router.post(
    "/{patient_id}/family-members",
    response_model=FamilyMemberRead,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar familiar vinculado al paciente (ADMIN o VOLUNTEER)",
)
def add_family_member(
    patient_id: int,
    body: FamilyMemberCreate,
    user: Annotated[User, Depends(get_current_user)],
    svc: Annotated[PatientFamilyService, Depends(get_patient_family_service)],
) -> FamilyMemberRead:
    roles = {r.role for r in user.roles}
    if not (roles & _STAFF_ROLES):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requiere rol de administrador o voluntario",
        )
    try:
        member = svc.add_family_member(
            user,
            patient_id,
            full_name=body.full_name,
            document_number=body.document_number,
            phone=body.phone,
            email=body.email,
        )
    except DocumentValidationError as exc:
        detail = str(exc)
        code = (
            status.HTTP_404_NOT_FOUND
            if detail == "Paciente no encontrado"
            else status.HTTP_400_BAD_REQUEST
        )
        raise HTTPException(status_code=code, detail=detail) from exc
    return _family_read(member)
