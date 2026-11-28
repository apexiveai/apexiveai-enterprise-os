"""Add persistent agent performance reviews.

Revision ID: 20261126_0004
Revises: 20261126_0003
"""

from alembic import op
import sqlalchemy as sa


revision = "20261126_0004"
down_revision = "20261126_0003"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "agent_performance_reviews",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("tenant_id", sa.String(100), nullable=False),
        sa.Column(
            "agent_id",
            sa.String(36),
            sa.ForeignKey("agent_definitions.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("reviewer_id", sa.String(100), nullable=False),
        sa.Column("period_start", sa.Date(), nullable=False),
        sa.Column("period_end", sa.Date(), nullable=False),
        sa.Column("rating", sa.Integer(), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("kpi_scores", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(
        "ix_agent_reviews_tenant_agent_created",
        "agent_performance_reviews",
        ["tenant_id", "agent_id", "created_at"],
    )


def downgrade():
    op.drop_table("agent_performance_reviews")
