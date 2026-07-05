"""Add Documentos menu items (DNI, boleta, receta)

Revision ID: 006_menu_documentos
Revises: 005_patient_nullable
Create Date: 2026-07-01

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "006_menu_documentos"
down_revision: Union[str, Sequence[str], None] = "005_patient_nullable"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

_PATHS = ["/app/documentos/dni", "/app/documentos/boleta", "/app/documentos/receta"]

_ITEMS = [
    ("/app/documentos/dni", "Registrar DNI", 15, "id-card"),
    ("/app/documentos/boleta", "Registrar boleta", 16, "receipt"),
    ("/app/documentos/receta", "Registrar receta", 17, "pill"),
]


def upgrade() -> None:
    bind = op.get_bind()
    for path, label, sort_order, icon in _ITEMS:
        r = bind.execute(
            sa.text(
                "INSERT INTO menu_items (parent_id, path, label, sort_order, icon, is_active) "
                "VALUES (NULL, :path, :label, :so, :icon, true) RETURNING id"
            ),
            {"path": path, "label": label, "so": sort_order, "icon": icon},
        )
        mid = int(r.scalar_one())
        for role in ("ADMIN", "VOLUNTEER"):
            bind.execute(
                sa.text(
                    "INSERT INTO menu_item_roles (menu_item_id, role) VALUES (:mid, :role)"
                ),
                {"mid": mid, "role": role},
            )


def downgrade() -> None:
    bind = op.get_bind()
    for path in _PATHS:
        bind.execute(
            sa.text("DELETE FROM menu_items WHERE path = :path"),
            {"path": path},
        )
