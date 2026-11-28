"""Create persistent industrial device registry.

Revision ID: 20261127_0006
Revises: 20261126_0005
"""

from alembic import op
import sqlalchemy as sa


revision = "20261127_0006"
down_revision = "20261126_0005"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "industrial_devices",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("tenant_id", sa.String(length=100), nullable=False),
        sa.Column("name", sa.String(length=150), nullable=False),
        sa.Column("device_type", sa.String(length=80), nullable=False),
        sa.Column("manufacturer", sa.String(length=120), nullable=True),
        sa.Column("model", sa.String(length=120), nullable=True),
        sa.Column("protocol", sa.String(length=40), nullable=False),
        sa.Column("endpoint", sa.String(length=500), nullable=True),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("metadata_json", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_industrial_devices_type", "industrial_devices", ["device_type"])
    op.create_index("ix_industrial_devices_status", "industrial_devices", ["status"])
    op.create_index("ix_industrial_devices_tenant", "industrial_devices", ["tenant_id"])


def downgrade():
    op.drop_table("industrial_devices")
