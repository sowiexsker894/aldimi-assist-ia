from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.domain.entities.menu_item import MenuItem
from app.domain.entities.menu_item_role import MenuItemRoleRow
from app.domain.entities.user import User
from app.domain.entities.user_patient import UserPatientRow
from app.domain.entities.user_role import UserRoleRow


class UserRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_document_number(self, document_number: str) -> User | None:
        stmt = (
            select(User)
            .where(User.document_number == document_number)
            .options(
                selectinload(User.roles),
                selectinload(User.patient_links),
            )
        )
        return self._session.scalars(stmt).first()

    def list_family_by_patient(self, patient_id: int, *, family_role: str) -> list[User]:
        stmt = (
            select(User)
            .join(UserPatientRow, UserPatientRow.user_id == User.id)
            .join(UserRoleRow, UserRoleRow.user_id == User.id)
            .where(UserPatientRow.patient_id == patient_id)
            .where(UserRoleRow.role == family_role)
            .options(selectinload(User.roles))
            .order_by(User.full_name, User.id)
        )
        return list(self._session.scalars(stmt).unique().all())

    def get_by_email(self, email: str) -> User | None:
        stmt = (
            select(User)
            .where(User.email == email)
            .options(
                selectinload(User.roles),
                selectinload(User.patient_links),
            )
        )
        return self._session.scalars(stmt).first()

    def get_by_id(self, user_id: int) -> User | None:
        stmt = (
            select(User)
            .where(User.id == user_id)
            .options(
                selectinload(User.roles),
                selectinload(User.patient_links),
            )
        )
        return self._session.scalars(stmt).first()

    def add(self, user: User) -> User:
        self._session.add(user)
        self._session.flush()
        return user

    def list_by_role(self, role: str) -> list[User]:
        stmt = (
            select(User)
            .join(UserRoleRow, UserRoleRow.user_id == User.id)
            .where(UserRoleRow.role == role)
            .options(selectinload(User.roles))
            .order_by(User.full_name, User.id)
        )
        return list(self._session.scalars(stmt).unique().all())

    def set_active(self, user_id: int, is_active: bool) -> User | None:
        user = self.get_by_id(user_id)
        if user is None:
            return None
        user.is_active = is_active
        self._session.flush()
        return user


class MenuRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def list_items_for_roles(self, roles: set[str]) -> list[MenuItem]:
        if not roles:
            return []
        stmt = (
            select(MenuItem)
            .distinct()
            .join(MenuItemRoleRow, MenuItemRoleRow.menu_item_id == MenuItem.id)
            .where(MenuItem.is_active.is_(True))
            .where(MenuItemRoleRow.role.in_(roles))
            .order_by(MenuItem.sort_order, MenuItem.id)
        )
        return list(self._session.scalars(stmt).all())
