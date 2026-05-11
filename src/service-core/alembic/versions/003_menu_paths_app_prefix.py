"""Prefix authenticated portal menu paths with /app

Revision ID: 003_menu_app_paths
Revises: 002_users_menu
Create Date: 2026-05-11

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "003_menu_app_paths"
down_revision: Union[str, Sequence[str], None] = "002_users_menu"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    bind = op.get_bind()
    mapping = [
        ("/", "/app"),
        ("/pacientes", "/app/pacientes"),
        ("/demo", "/app/demo"),
        ("/admin/volunteers", "/app/admin/volunteers"),
    ]
    for old, new in mapping:
        bind.execute(
            sa.text("UPDATE menu_items SET path = :new WHERE path = :old"),
            {"new": new, "old": old},
        )


def downgrade() -> None:
    bind = op.get_bind()
    mapping = [
        ("/app", "/"),
        ("/app/pacientes", "/pacientes"),
        ("/app/demo", "/demo"),
        ("/app/admin/volunteers", "/admin/volunteers"),
    ]
    for new, old in mapping:
        bind.execute(
            sa.text("UPDATE menu_items SET path = :old WHERE path = :new"),
            {"new": new, "old": old},
        )
