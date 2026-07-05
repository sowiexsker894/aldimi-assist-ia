import secrets
import uuid

from app.core.document_exceptions import DocumentValidationError
from app.core.security import hash_password
from app.domain.entities.user import User
from app.domain.entities.user_role import UserRoleRow
from app.domain.enums import UserRole
from app.infrastructure.repositories.patient_repository import PatientRepository
from app.infrastructure.repositories.user_repository import UserRepository

_STAFF_ROLES = {UserRole.ADMIN.value, UserRole.VOLUNTEER.value}


class PatientFamilyService:
    def __init__(
        self,
        patients: PatientRepository,
        users: UserRepository,
    ) -> None:
        self._patients = patients
        self._users = users

    def _require_staff(self, actor: User) -> None:
        roles = {r.role for r in actor.roles}
        if not (roles & _STAFF_ROLES):
            raise DocumentValidationError(
                "Se requiere rol de administrador o voluntario",
            )

    def _require_patient(self, patient_id: int):
        patient = self._patients.get_by_id(patient_id)
        if patient is None:
            raise DocumentValidationError("Paciente no encontrado")
        return patient

    @staticmethod
    def _generated_email(document_number: str | None) -> str:
        if document_number and document_number.strip():
            return f"{document_number.strip()}@familia.aldimi.local"
        return f"fam_{uuid.uuid4().hex[:12]}@familia.aldimi.local"

    def list_family_members(self, actor: User, patient_id: int) -> list[User]:
        self._require_staff(actor)
        self._require_patient(patient_id)
        return self._users.list_family_by_patient(
            patient_id,
            family_role=UserRole.FAMILY.value,
        )

    def add_family_member(
        self,
        actor: User,
        patient_id: int,
        *,
        full_name: str,
        document_number: str | None = None,
        phone: str | None = None,
        email: str | None = None,
    ) -> User:
        self._require_staff(actor)
        self._require_patient(patient_id)

        name = full_name.strip()
        if not name:
            raise DocumentValidationError("El nombre del familiar es obligatorio")

        doc = document_number.strip() if document_number else None
        user: User | None = None
        if doc:
            user = self._users.get_by_document_number(doc)

        if user is None:
            email_norm = email.strip().lower() if email else self._generated_email(doc)
            if self._users.get_by_email(email_norm):
                raise DocumentValidationError("El correo del familiar ya está registrado")
            user = User(
                email=email_norm,
                hashed_password=hash_password(secrets.token_urlsafe(24)),
                full_name=name,
                phone=phone.strip() if phone else None,
                document_number=doc,
                is_active=False,
            )
            user.roles.append(UserRoleRow(role=UserRole.FAMILY.value))
            self._users.add(user)
        elif UserRole.FAMILY.value not in {r.role for r in user.roles}:
            user.roles.append(UserRoleRow(role=UserRole.FAMILY.value))

        if self._patients.has_user_patient_link(user.id, patient_id):
            raise DocumentValidationError("El familiar ya está vinculado a este paciente")

        self._patients.link_user_to_patient(user.id, patient_id)
        return user
