"""make patient_id nullable on document tables

Revision ID: 005_patient_nullable
Revises: 004_documents
Create Date: 2026-07-01

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "005_patient_nullable"
down_revision: Union[str, Sequence[str], None] = "004_documents"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "analysis_sessions",
        "patient_id",
        existing_type=sa.Integer(),
        nullable=True,
    )
    op.alter_column(
        "documents",
        "patient_id",
        existing_type=sa.Integer(),
        nullable=True,
    )


def downgrade() -> None:
    op.alter_column(
        "documents",
        "patient_id",
        existing_type=sa.Integer(),
        nullable=False,
    )
    op.alter_column(
        "analysis_sessions",
        "patient_id",
        existing_type=sa.Integer(),
        nullable=False,
    )
