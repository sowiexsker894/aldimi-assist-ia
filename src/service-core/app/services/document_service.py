from datetime import datetime, timedelta, timezone
import uuid
from typing import Any

from app.core.auth_exceptions import ForbiddenActionError
from app.core.document_exceptions import (
    DocumentAnalysisRejectedError,
    DocumentSessionError,
    DocumentValidationError,
)
from app.domain.entities.document import AnalysisSession, Document
from app.domain.entities.patient import Patient
from app.domain.entities.user import User
from app.domain.enums import UserRole
from app.infrastructure.repositories.document_repository import (
    AnalysisSessionRepository,
    DocumentRepository,
)
from app.infrastructure.repositories.patient_repository import PatientRepository
from app.infrastructure.repositories.prescription_repository import PrescriptionRepository
from app.infrastructure.repositories.receipt_repository import ReceiptRepository
from app.services.document_mappers import (
    full_name_from_dni,
    patient_fields_from_dni,
    prescription_fields_from_receta,
    receipt_fields_from_boleta,
)
from app.services.ports.vision import VisionClientPort

SESSION_TTL_MINUTES = 30

_REQUIRED_FIELDS: dict[str, list[str]] = {
    "dni": ["dni_number"],
    "receta": ["paciente_nombre"],
    "boleta": ["total", "fecha_emision"],
}


class DocumentService:
    def __init__(
        self,
        patient_repo: PatientRepository,
        session_repo: AnalysisSessionRepository,
        document_repo: DocumentRepository,
        vision_client: VisionClientPort,
        prescription_repo: PrescriptionRepository,
        receipt_repo: ReceiptRepository,
    ) -> None:
        self._patient_repo = patient_repo
        self._session_repo = session_repo
        self._document_repo = document_repo
        self._vision_client = vision_client
        self._prescription_repo = prescription_repo
        self._receipt_repo = receipt_repo

    def analyze_document(
        self,
        user: User,
        *,
        document_type: str,
        images_base64: list[str],
        patient_id: int | None = None,
    ) -> dict[str, Any]:
        if document_type in ("dni", "boleta") and patient_id is not None:
            raise DocumentValidationError(
                f"patient_id no debe enviarse para document_type={document_type}"
            )

        if document_type == "receta" and patient_id is not None:
            patient = self._patient_repo.get_by_id(patient_id)
            if patient is None:
                raise DocumentValidationError("Paciente no encontrado")
            self._ensure_patient_access(user, patient_id)

        vision_response = self._vision_client.analyze_document(
            document_type=document_type,
            images_base64=images_base64,
        )

        if vision_response.get("status") == "rejected":
            rejection = vision_response.get("rejection") or {}
            if isinstance(rejection, dict):
                code = str(rejection.get("code", "wrong_document"))
                message = str(rejection.get("message", "Imagen rechazada"))
            else:
                code = "wrong_document"
                message = str(rejection)
            raise DocumentAnalysisRejectedError(code=code, message=message)

        draft = vision_response.get("draft")
        if not isinstance(draft, dict):
            raise DocumentValidationError("Respuesta de vision sin draft válido")

        warnings = vision_response.get("warnings") or []
        if not isinstance(warnings, list):
            warnings = []

        metadata = vision_response.get("metadata") or {}
        gatekeeper_label = metadata.get("gatekeeper_label") if isinstance(metadata, dict) else None
        gatekeeper_score = metadata.get("gatekeeper_score") if isinstance(metadata, dict) else None

        expires_at = datetime.now(timezone.utc) + timedelta(minutes=SESSION_TTL_MINUTES)
        session = self._session_repo.create(
            user_id=user.id,
            patient_id=patient_id,
            document_type=document_type,
            draft=draft,
            warnings=[str(w) for w in warnings],
            gatekeeper_label=str(gatekeeper_label) if gatekeeper_label else None,
            gatekeeper_score=float(gatekeeper_score) if gatekeeper_score is not None else None,
            expires_at=expires_at,
        )

        return {
            "analysis_session_id": str(session.id),
            "document_type": document_type,
            "draft": draft,
            "warnings": [str(w) for w in warnings],
            "metadata": metadata if isinstance(metadata, dict) else {},
        }

    def save_dni_document(
        self,
        user: User,
        *,
        analysis_session_id: uuid.UUID,
        confirmed_fields: dict[str, Any],
    ) -> Document:
        session = self._load_session_for_save(
            user,
            analysis_session_id=analysis_session_id,
            expected_document_type="dni",
        )
        self._validate_confirmed_fields("dni", confirmed_fields)

        patient = self._upsert_patient_from_dni(confirmed_fields)
        self._link_user_to_patient(user, patient.id)

        document = self._document_repo.create(
            patient_id=patient.id,
            document_type="dni",
            confirmed_fields=confirmed_fields,
            created_by=user.id,
            analysis_session_id=session.id,
        )
        self._session_repo.mark_consumed(session)
        return document

    def save_boleta_document(
        self,
        user: User,
        *,
        analysis_session_id: uuid.UUID,
        confirmed_fields: dict[str, Any],
    ) -> Document:
        session = self._load_session_for_save(
            user,
            analysis_session_id=analysis_session_id,
            expected_document_type="boleta",
        )
        self._validate_confirmed_fields("boleta", confirmed_fields)

        document = self._document_repo.create(
            patient_id=None,
            document_type="boleta",
            confirmed_fields=confirmed_fields,
            created_by=user.id,
            analysis_session_id=session.id,
        )
        self._receipt_repo.create(
            patient_id=None,
            document_id=document.id,
            created_by=user.id,
            **receipt_fields_from_boleta(confirmed_fields),
        )
        self._session_repo.mark_consumed(session)
        return document

    def save_receta_document(
        self,
        user: User,
        *,
        analysis_session_id: uuid.UUID,
        patient_id: int,
        confirmed_fields: dict[str, Any],
    ) -> Document:
        session = self._load_session_for_save(
            user,
            analysis_session_id=analysis_session_id,
            expected_document_type="receta",
        )
        if session.patient_id is not None and session.patient_id != patient_id:
            raise DocumentSessionError("El paciente no coincide con la sesión de análisis")

        patient = self._patient_repo.get_by_id(patient_id)
        if patient is None:
            raise DocumentValidationError("Paciente no encontrado")

        self._ensure_patient_access(user, patient_id)
        self._validate_confirmed_fields("receta", confirmed_fields)

        document = self._document_repo.create(
            patient_id=patient_id,
            document_type="receta",
            confirmed_fields=confirmed_fields,
            created_by=user.id,
            analysis_session_id=session.id,
        )
        self._prescription_repo.create(
            patient_id=patient_id,
            document_id=document.id,
            created_by=user.id,
            **prescription_fields_from_receta(confirmed_fields),
        )
        self._session_repo.mark_consumed(session)
        return document

    def _load_session_for_save(
        self,
        user: User,
        *,
        analysis_session_id: uuid.UUID,
        expected_document_type: str,
    ) -> AnalysisSession:
        session = self._session_repo.get_by_id(analysis_session_id)
        if session is None:
            raise DocumentSessionError("Sesión de análisis no encontrada")
        if session.consumed:
            raise DocumentSessionError("La sesión de análisis ya fue utilizada")
        if session.expires_at < datetime.now(timezone.utc):
            raise DocumentSessionError("La sesión de análisis expiró")
        if session.user_id != user.id:
            raise ForbiddenActionError("No puede guardar una sesión iniciada por otro usuario")
        if session.document_type != expected_document_type:
            raise DocumentSessionError(
                f"La sesión corresponde a {session.document_type}, no a {expected_document_type}"
            )
        return session

    def _upsert_patient_from_dni(self, confirmed_fields: dict[str, Any]) -> Patient:
        fields = patient_fields_from_dni(confirmed_fields)
        full_name = full_name_from_dni(confirmed_fields)
        dni = fields.get("dni")

        existing = self._patient_repo.get_by_dni(dni) if dni else None
        if existing is not None:
            existing.full_name = full_name
            for key, value in fields.items():
                if value is not None:
                    setattr(existing, key, value)
            return existing

        return self._patient_repo.add(Patient(full_name=full_name, **fields))

    def _link_user_to_patient(self, user: User, patient_id: int) -> None:
        roles = {r.role for r in user.roles}
        if UserRole.ADMIN.value in roles:
            return
        linked = {link.patient_id for link in user.patient_links}
        if patient_id in linked:
            return
        self._patient_repo.link_user_to_patient(user.id, patient_id)

    def _ensure_patient_access(self, user: User, patient_id: int) -> None:
        roles = {r.role for r in user.roles}
        if UserRole.ADMIN.value in roles:
            return
        linked = {link.patient_id for link in user.patient_links}
        if patient_id not in linked:
            raise ForbiddenActionError("No tiene acceso a este paciente")

    def _validate_confirmed_fields(
        self, document_type: str, confirmed_fields: dict[str, Any]
    ) -> None:
        required = _REQUIRED_FIELDS.get(document_type, [])
        for field in required:
            value = confirmed_fields.get(field)
            if value is None or (isinstance(value, str) and not value.strip()):
                raise DocumentValidationError(
                    f"Campo obligatorio faltante: {field}"
                )
