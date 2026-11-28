"""Create persistent industry solution work records.

Revision ID: 20261126_0005
Revises: 20261126_0004
"""

from alembic import op
import sqlalchemy as sa


revision = "20261126_0005"
down_revision = "20261126_0004"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "industry_solution_records",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("tenant_id", sa.String(100), nullable=False),
        sa.Column("solution_key", sa.String(40), nullable=False),
        sa.Column("title", sa.String(250), nullable=False),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("created_by", sa.String(100), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(
        "ix_industry_records_tenant_solution_updated",
        "industry_solution_records",
        ["tenant_id", "solution_key", "updated_at"],
    )
    op.create_index(
        "ix_industry_records_tenant_solution_status",
        "industry_solution_records",
        ["tenant_id", "solution_key", "status"],
    )


def downgrade():
    op.drop_table("industry_solution_records")
