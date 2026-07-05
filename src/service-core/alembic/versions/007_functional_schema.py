"""enrich patients/users and add prescriptions, receipts, sentiment_reports

Revision ID: 007_functional_schema
Revises: 006_menu_documentos
Create Date: 2026-07-01

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "007_functional_schema"
down_revision: Union[str, Sequence[str], None] = "006_menu_documentos"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # --- Enriquecer patients ---
    op.add_column("patients", sa.Column("dni", sa.String(length=8), nullable=True))
    op.add_column("patients", sa.Column("primer_apellido", sa.String(length=120), nullable=True))
    op.add_column("patients", sa.Column("segundo_apellido", sa.String(length=120), nullable=True))
    op.add_column("patients", sa.Column("primer_nombre", sa.String(length=120), nullable=True))
    op.add_column("patients", sa.Column("segundo_nombre", sa.String(length=120), nullable=True))
    op.add_column("patients", sa.Column("sexo", sa.String(length=16), nullable=True))
    op.add_column("patients", sa.Column("fecha_nacimiento", sa.Date(), nullable=True))
    op.add_column("patients", sa.Column("nacionalidad", sa.String(length=64), nullable=True))
    op.add_column("patients", sa.Column("estado_civil", sa.String(length=32), nullable=True))
    op.add_column("patients", sa.Column("direccion", sa.String(length=512), nullable=True))
    op.add_column("patients", sa.Column("ubigeo", sa.String(length=6), nullable=True))
    op.add_column(
        "patients",
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    op.add_column(
        "patients",
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    op.create_unique_constraint("uq_patients_dni", "patients", ["dni"])

    # --- Perfil de voluntario en users ---
    op.add_column("users", sa.Column("phone", sa.String(length=32), nullable=True))
    op.add_column("users", sa.Column("document_number", sa.String(length=32), nullable=True))

    # --- prescriptions (receta normalizada) ---
    op.create_table(
        "prescriptions",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("patient_id", sa.Integer(), nullable=True),
        sa.Column("document_id", sa.Integer(), nullable=True),
        sa.Column("medico", sa.String(length=255), nullable=True),
        sa.Column("cedula_medico", sa.String(length=64), nullable=True),
        sa.Column("paciente_nombre", sa.String(length=255), nullable=True),
        sa.Column("medicamentos", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("indicaciones", sa.Text(), nullable=True),
        sa.Column("nombre_clinica", sa.String(length=255), nullable=True),
        sa.Column("fecha", sa.Date(), nullable=True),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["patient_id"], ["patients.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["document_id"], ["documents.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )

    # --- receipts (boleta normalizada) ---
    op.create_table(
        "receipts",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("patient_id", sa.Integer(), nullable=True),
        sa.Column("document_id", sa.Integer(), nullable=True),
        sa.Column("monto_recibido", sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column("nombre", sa.String(length=255), nullable=True),
        sa.Column("fecha", sa.Date(), nullable=True),
        sa.Column("medio_pago", sa.String(length=64), nullable=True),
        sa.Column("numero_operacion", sa.String(length=64), nullable=True),
        sa.Column("created_by", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["patient_id"], ["patients.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["document_id"], ["documents.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["created_by"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )

    # --- sentiment_reports (NLP) ---
    op.create_table(
        "sentiment_reports",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("patient_id", sa.Integer(), nullable=True),
        sa.Column("text_content", sa.Text(), nullable=False),
        sa.Column("sentiment_score", sa.Float(), nullable=True),
        sa.Column("sentiment_label", sa.String(length=16), nullable=True),
        sa.Column("alert_flag", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["patient_id"], ["patients.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("sentiment_reports")
    op.drop_table("receipts")
    op.drop_table("prescriptions")

    op.drop_column("users", "document_number")
    op.drop_column("users", "phone")

    op.drop_constraint("uq_patients_dni", "patients", type_="unique")
    op.drop_column("patients", "updated_at")
    op.drop_column("patients", "created_at")
    op.drop_column("patients", "ubigeo")
    op.drop_column("patients", "direccion")
    op.drop_column("patients", "estado_civil")
    op.drop_column("patients", "nacionalidad")
    op.drop_column("patients", "fecha_nacimiento")
    op.drop_column("patients", "sexo")
    op.drop_column("patients", "segundo_nombre")
    op.drop_column("patients", "primer_nombre")
    op.drop_column("patients", "segundo_apellido")
    op.drop_column("patients", "primer_apellido")
    op.drop_column("patients", "dni")
