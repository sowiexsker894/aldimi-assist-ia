from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_admin_volunteer_service, require_admin
from app.api.schemas.auth import (
    CreateVolunteerRequest,
    CreateVolunteerResponse,
    UpdateVolunteerStatusRequest,
    VolunteerRead,
)
from app.core.auth_exceptions import ForbiddenActionError
from app.domain.entities.user import User
from app.services.auth_service import AdminVolunteerService

router = APIRouter()


def _volunteer_read(user: User) -> VolunteerRead:
    return VolunteerRead(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        phone=user.phone,
        document_number=user.document_number,
        is_active=user.is_active,
        roles=[r.role for r in user.roles],
    )


@router.get(
    "/volunteers",
    response_model=list[VolunteerRead],
    summary="Listar voluntarios (solo ADMIN)",
)
def list_volunteers(
    admin: Annotated[User, Depends(require_admin)],
    svc: Annotated[AdminVolunteerService, Depends(get_admin_volunteer_service)],
) -> list[VolunteerRead]:
    try:
        volunteers = svc.list_volunteers(admin)
    except ForbiddenActionError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        ) from exc
    return [_volunteer_read(v) for v in volunteers]


@router.post(
    "/volunteers",
    response_model=CreateVolunteerResponse,
    summary="Alta de voluntario (solo ADMIN)",
)
def create_volunteer(
    body: CreateVolunteerRequest,
    admin: Annotated[User, Depends(require_admin)],
    svc: Annotated[AdminVolunteerService, Depends(get_admin_volunteer_service)],
) -> CreateVolunteerResponse:
    try:
        user = svc.create_volunteer(
            actor=admin,
            email=body.email,
            password=body.password,
            full_name=body.full_name,
            phone=body.phone,
            document_number=body.document_number,
        )
    except ForbiddenActionError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        ) from exc
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    return CreateVolunteerResponse(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        phone=user.phone,
        document_number=user.document_number,
        roles=[r.role for r in user.roles],
    )


@router.patch(
    "/volunteers/{user_id}",
    response_model=VolunteerRead,
    summary="Activar o desactivar voluntario (solo ADMIN)",
)
def update_volunteer_status(
    user_id: int,
    body: UpdateVolunteerStatusRequest,
    admin: Annotated[User, Depends(require_admin)],
    svc: Annotated[AdminVolunteerService, Depends(get_admin_volunteer_service)],
) -> VolunteerRead:
    try:
        user = svc.set_volunteer_active(
            actor=admin,
            user_id=user_id,
            is_active=body.is_active,
        )
    except ForbiddenActionError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        ) from exc
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    return _volunteer_read(user)
