from sqlalchemy import ForeignKey, PrimaryKeyConstraint, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.base import Base


class MenuItemRoleRow(Base):
    __tablename__ = "menu_item_roles"
    __table_args__ = (PrimaryKeyConstraint("menu_item_id", "role"),)

    menu_item_id: Mapped[int] = mapped_column(
        ForeignKey("menu_items.id", ondelete="CASCADE"),
        nullable=False,
    )
    role: Mapped[str] = mapped_column(String(32), nullable=False)

    menu_item: Mapped["MenuItem"] = relationship("MenuItem", back_populates="role_rows")
