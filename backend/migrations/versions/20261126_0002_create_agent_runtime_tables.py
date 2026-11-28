"""Create persistent agent runtime tables.

Revision ID: 20261126_0002
Revises: 20261126_0001
"""

from alembic import op
import sqlalchemy as sa


revision = "20261126_0002"
down_revision = "20261126_0001"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "agent_definitions",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("tenant_id", sa.String(100), nullable=False),
        sa.Column("slug", sa.String(100), nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("model", sa.String(200), nullable=False),
        sa.Column("system_prompt", sa.Text(), nullable=False),
        sa.Column("allowed_tools", sa.JSON(), nullable=False),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("created_by", sa.String(100), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("tenant_id", "slug", name="uq_agent_tenant_slug"),
    )
    op.create_index(
        "ix_agent_definitions_tenant_status",
        "agent_definitions",
        ["tenant_id", "status"],
    )

    op.create_table(
        "agent_memories",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("tenant_id", sa.String(100), nullable=False),
        sa.Column(
            "agent_id",
            sa.String(36),
            sa.ForeignKey("agent_definitions.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("memory_key", sa.String(200), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("labels", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(
        "ix_agent_memories_tenant_agent_created",
        "agent_memories",
        ["tenant_id", "agent_id", "created_at"],
    )

    op.create_table(
        "agent_executions",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("tenant_id", sa.String(100), nullable=False),
        sa.Column(
            "agent_id",
            sa.String(36),
            sa.ForeignKey("agent_definitions.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("model", sa.String(200), nullable=False),
        sa.Column("prompt", sa.Text(), nullable=False),
        sa.Column("output", sa.Text(), nullable=True),
        sa.Column("error", sa.Text(), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(
        "ix_agent_executions_tenant_agent_created",
        "agent_executions",
        ["tenant_id", "agent_id", "created_at"],
    )
    op.create_index(
        "ix_agent_executions_status_created",
        "agent_executions",
        ["status", "created_at"],
    )

    op.create_table(
        "agent_audit_logs",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("tenant_id", sa.String(100), nullable=False),
        sa.Column(
            "agent_id",
            sa.String(36),
            sa.ForeignKey("agent_definitions.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("actor_id", sa.String(100), nullable=False),
        sa.Column("action", sa.String(100), nullable=False),
        sa.Column("resource_type", sa.String(80), nullable=False),
        sa.Column("resource_id", sa.String(100), nullable=True),
        sa.Column("details", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(
        "ix_agent_audit_tenant_created",
        "agent_audit_logs",
        ["tenant_id", "created_at"],
    )
    op.create_index(
        "ix_agent_audit_resource",
        "agent_audit_logs",
        ["resource_type", "resource_id"],
    )

    op.create_table(
        "agent_teams",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("tenant_id", sa.String(100), nullable=False),
        sa.Column("slug", sa.String(100), nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("member_agent_ids", sa.JSON(), nullable=False),
        sa.Column("created_by", sa.String(100), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint("tenant_id", "slug", name="uq_agent_team_tenant_slug"),
    )
    op.create_index("ix_agent_teams_tenant", "agent_teams", ["tenant_id"])

    op.create_table(
        "agent_team_executions",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("tenant_id", sa.String(100), nullable=False),
        sa.Column(
            "team_id",
            sa.String(36),
            sa.ForeignKey("agent_teams.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("prompt", sa.Text(), nullable=False),
        sa.Column("output", sa.JSON(), nullable=False),
        sa.Column("error", sa.Text(), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(
        "ix_agent_team_executions_tenant_created",
        "agent_team_executions",
        ["tenant_id", "created_at"],
    )
    op.create_index(
        "ix_agent_team_executions_status_created",
        "agent_team_executions",
        ["status", "created_at"],
    )


def downgrade():
    op.drop_table("agent_team_executions")
    op.drop_table("agent_teams")
    op.drop_table("agent_audit_logs")
    op.drop_table("agent_executions")
    op.drop_table("agent_memories")
    op.drop_table("agent_definitions")
