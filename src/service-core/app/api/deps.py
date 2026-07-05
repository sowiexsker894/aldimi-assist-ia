from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.core.security import decode_token
from app.domain.entities.user import User
from app.domain.enums import UserRole
from app.infrastructure.clients.nlp_http_client import NlpHttpClient
from app.infrastructure.clients.vision_http_client import VisionHttpClient
from app.infrastructure.persistence.session import get_db
from app.infrastructure.repositories.document_repository import (
    AnalysisSessionRepository,
    DocumentRepository,
)
from app.infrastructure.repositories.patient_repository import PatientRepository
from app.infrastructure.repositories.prescription_repository import PrescriptionRepository
from app.infrastructure.repositories.receipt_repository import ReceiptRepository
from app.infrastructure.repositories.sentiment_repository import SentimentReportRepository
from app.infrastructure.repositories.user_repository import MenuRepository, UserRepository
from app.services.auth_service import AdminVolunteerService, AuthService
from app.services.daily_report_service import DailyReportService
from app.services.patient_family_service import PatientFamilyService
from app.services.document_service import DocumentService
from app.services.patient_service import PatientService

security = HTTPBearer()


def get_user_repository(
    db: Annotated[Session, Depends(get_db)],
) -> UserRepository:
    return UserRepository(db)


def get_menu_repository(
    db: Annotated[Session, Depends(get_db)],
) -> MenuRepository:
    return MenuRepository(db)


def get_auth_service(
    users: Annotated[UserRepository, Depends(get_user_repository)],
    menus: Annotated[MenuRepository, Depends(get_menu_repository)],
) -> AuthService:
    return AuthService(users, menus)


def get_admin_volunteer_service(
    users: Annotated[UserRepository, Depends(get_user_repository)],
) -> AdminVolunteerService:
    return AdminVolunteerService(users)


def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    users: Annotated[UserRepository, Depends(get_user_repository)],
) -> User:
    try:
        payload = decode_token(credentials.credentials)
        uid = int(payload["sub"])
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
        ) from exc
    user = users.get_by_id(uid)
    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no autorizado",
        )
    return user


def require_admin(user: Annotated[User, Depends(get_current_user)]) -> User:
    roles = {r.role for r in user.roles}
    if UserRole.ADMIN.value not in roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Se requiere rol de administrador",
        )
    return user


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


def get_analysis_session_repository(
    db: Annotated[Session, Depends(get_db)],
) -> AnalysisSessionRepository:
    return AnalysisSessionRepository(db)


def get_document_repository(
    db: Annotated[Session, Depends(get_db)],
) -> DocumentRepository:
    return DocumentRepository(db)


def get_prescription_repository(
    db: Annotated[Session, Depends(get_db)],
) -> PrescriptionRepository:
    return PrescriptionRepository(db)


def get_receipt_repository(
    db: Annotated[Session, Depends(get_db)],
) -> ReceiptRepository:
    return ReceiptRepository(db)


def get_sentiment_report_repository(
    db: Annotated[Session, Depends(get_db)],
) -> SentimentReportRepository:
    return SentimentReportRepository(db)


def get_daily_report_service(
    patient_repo: Annotated[PatientRepository, Depends(get_patient_repository)],
    report_repo: Annotated[SentimentReportRepository, Depends(get_sentiment_report_repository)],
) -> DailyReportService:
    return DailyReportService(patient_repo, report_repo)


def get_patient_family_service(
    patient_repo: Annotated[PatientRepository, Depends(get_patient_repository)],
    users: Annotated[UserRepository, Depends(get_user_repository)],
) -> PatientFamilyService:
    return PatientFamilyService(patient_repo, users)


def get_document_service(
    patient_repo: Annotated[PatientRepository, Depends(get_patient_repository)],
    session_repo: Annotated[AnalysisSessionRepository, Depends(get_analysis_session_repository)],
    document_repo: Annotated[DocumentRepository, Depends(get_document_repository)],
    vision: Annotated[VisionHttpClient, Depends(get_vision_http_client)],
    prescription_repo: Annotated[PrescriptionRepository, Depends(get_prescription_repository)],
    receipt_repo: Annotated[ReceiptRepository, Depends(get_receipt_repository)],
) -> DocumentService:
    return DocumentService(
        patient_repo,
        session_repo,
        document_repo,
        vision,
        prescription_repo,
        receipt_repo,
    )

