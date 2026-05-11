from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_auth_service, get_current_user
from app.api.schemas.auth import LoginRequest, LoginResponse, MeResponse
from app.core.auth_exceptions import InvalidCredentialsError, UserInactiveError
from app.domain.entities.user import User
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/login", response_model=LoginResponse, summary="Iniciar sesión (JWT)")
def login(
    body: LoginRequest,
    auth: Annotated[AuthService, Depends(get_auth_service)],
) -> LoginResponse:
    try:
        token, user, menu = auth.login(body.email, body.password)
    except InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas",
        )
    except UserInactiveError as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(exc),
        ) from exc
    return LoginResponse(access_token=token, user=user, menu=menu)


@router.get("/me", response_model=MeResponse, summary="Usuario actual y menú")
def me(
    auth: Annotated[AuthService, Depends(get_auth_service)],
    user: Annotated[User, Depends(get_current_user)],
) -> MeResponse:
    return MeResponse(user=auth.user_summary(user), menu=auth.menu_for_user(user))
