"""users, roles, menu, seeds

Revision ID: 002_users_menu
Revises: 001_initial
Create Date: 2026-05-11

"""

from typing import Sequence, Union

import bcrypt
from alembic import op
import sqlalchemy as sa

revision: str = "002_users_menu"
down_revision: Union[str, Sequence[str], None] = "001_initial"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("hashed_password", sa.String(length=512), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )
    op.create_index("ix_users_email", "users", ["email"], unique=False)

    op.create_table(
        "user_roles",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("role", sa.String(length=32), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_id", "role"),
    )

    op.create_table(
        "user_patients",
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("patient_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["patient_id"], ["patients.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("user_id", "patient_id"),
    )

    op.create_table(
        "menu_items",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("parent_id", sa.Integer(), nullable=True),
        sa.Column("path", sa.String(length=512), nullable=False),
        sa.Column("label", sa.String(length=255), nullable=False),
        sa.Column("sort_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("icon", sa.String(length=64), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.ForeignKeyConstraint(["parent_id"], ["menu_items.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_table(
        "menu_item_roles",
        sa.Column("menu_item_id", sa.Integer(), nullable=False),
        sa.Column("role", sa.String(length=32), nullable=False),
        sa.ForeignKeyConstraint(["menu_item_id"], ["menu_items.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("menu_item_id", "role"),
    )

    bind = op.get_bind()
    admin_hash = bcrypt.hashpw(
        b"AdminDev123!",
        bcrypt.gensalt(),
    ).decode("utf-8")
    row = bind.execute(
        sa.text(
            "INSERT INTO users (email, hashed_password, full_name, is_active) "
            "VALUES (:email, :hp, :fn, true) RETURNING id"
        ),
        {
            "email": "admin@aldimi.local",
            "hp": admin_hash,
            "fn": "Administrador (dev)",
        },
    )
    admin_id = row.scalar_one()

    bind.execute(
        sa.text("INSERT INTO user_roles (user_id, role) VALUES (:id, 'ADMIN')"),
        {"id": admin_id},
    )

    # menu items
    menu_rows = [
        (None, "/app", "Inicio", 0, "home"),
        (None, "/app/pacientes", "Pacientes", 10, "users"),
        (None, "/app/demo", "Demostración UI", 20, "layout"),
        (None, "/app/admin/volunteers", "Alta voluntarios", 30, "user-plus"),
    ]
    mids: list[int] = []
    for parent_id, path, label, sort_order, icon in menu_rows:
        r = bind.execute(
            sa.text(
                "INSERT INTO menu_items (parent_id, path, label, sort_order, icon, is_active) "
                "VALUES (:p, :path, :label, :so, :icon, true) RETURNING id"
            ),
            {
                "p": parent_id,
                "path": path,
                "label": label,
                "so": sort_order,
                "icon": icon,
            },
        )
        mids.append(int(r.scalar_one()))

    roles_by_item = [
        (mids[0], ["ADMIN", "VOLUNTEER"]),
        (mids[1], ["ADMIN", "VOLUNTEER"]),
        (mids[2], ["ADMIN", "VOLUNTEER"]),
        (mids[3], ["ADMIN"]),
    ]
    for mid, roles in roles_by_item:
        for role in roles:
            bind.execute(
                sa.text(
                    "INSERT INTO menu_item_roles (menu_item_id, role) VALUES (:mid, :role)"
                ),
                {"mid": mid, "role": role},
            )


def downgrade() -> None:
    op.drop_table("menu_item_roles")
    op.drop_table("menu_items")
    op.drop_table("user_patients")
    op.drop_table("user_roles")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_table("users")
