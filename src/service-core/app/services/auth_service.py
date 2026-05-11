from app.api.schemas.auth import MenuNodeDto, UserSummaryDto
from app.core.auth_exceptions import (
    ForbiddenActionError,
    InvalidCredentialsError,
    UserInactiveError,
)
from app.core.security import create_access_token, hash_password, verify_password
from app.domain.entities.user import User
from app.domain.entities.user_role import UserRoleRow
from app.domain.enums import UserRole
from app.infrastructure.repositories.user_repository import MenuRepository, UserRepository
from app.services.menu_builder import build_menu_tree


class AuthService:
    def __init__(
        self,
        users: UserRepository,
        menus: MenuRepository,
    ) -> None:
        self._users = users
        self._menus = menus

    def _roles_set(self, user: User) -> set[str]:
        return {r.role for r in user.roles}

    def user_summary(self, user: User) -> UserSummaryDto:
        return UserSummaryDto(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            roles=sorted(self._roles_set(user)),
        )

    def menu_for_user(self, user: User) -> list[MenuNodeDto]:
        items = self._menus.list_items_for_roles(self._roles_set(user))
        return build_menu_tree(items)

    def login(self, email: str, password: str) -> tuple[str, UserSummaryDto, list[MenuNodeDto]]:
        user = self._users.get_by_email(email.strip().lower())
        if user is None or not verify_password(password, user.hashed_password):
            raise InvalidCredentialsError("Credenciales inválidas")
        if not user.is_active:
            raise UserInactiveError("Cuenta desactivada. Contacte a administración.")
        token = create_access_token(
            subject=str(user.id),
            claims={"email": user.email, "roles": sorted(self._roles_set(user))},
        )
        return token, self.user_summary(user), self.menu_for_user(user)


class AdminVolunteerService:
    def __init__(self, users: UserRepository) -> None:
        self._users = users

    def create_volunteer(
        self,
        *,
        actor: User,
        email: str,
        password: str,
        full_name: str,
    ) -> User:
        if UserRole.ADMIN.value not in {r.role for r in actor.roles}:
            raise ForbiddenActionError("Solo administradores pueden crear voluntarios.")
        email_norm = email.strip().lower()
        if self._users.get_by_email(email_norm):
            raise ValueError("El correo ya está registrado.")
        user = User(
            email=email_norm,
            hashed_password=hash_password(password),
            full_name=full_name.strip(),
            is_active=True,
        )
        user.roles.append(UserRoleRow(role=UserRole.VOLUNTEER.value))
        self._users.add(user)
        return user
