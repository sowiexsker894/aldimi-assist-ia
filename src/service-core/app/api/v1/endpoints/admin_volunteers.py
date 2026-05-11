from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_admin_volunteer_service, require_admin
from app.api.schemas.auth import CreateVolunteerRequest, CreateVolunteerResponse
from app.core.auth_exceptions import ForbiddenActionError
from app.domain.entities.user import User
from app.services.auth_service import AdminVolunteerService

router = APIRouter()


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
        roles=[r.role for r in user.roles],
    )
