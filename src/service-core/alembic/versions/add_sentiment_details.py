"""add sentiment details to sentiment reports

Revision ID: add_sentiment_details
Revises: 007_functional_schema
Create Date: 2026-07-08

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "add_sentiment_details"
down_revision: Union[str, None] = "007_functional_schema"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "sentiment_reports",
        sa.Column("sentiment_details", sa.JSON(), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("sentiment_reports", "sentiment_details")
