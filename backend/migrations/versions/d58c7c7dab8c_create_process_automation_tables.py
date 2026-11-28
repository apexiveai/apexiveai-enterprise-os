
"""Create Process Automation tables.

Revision ID: 20261126_0001
"""

from alembic import op
import sqlalchemy as sa


revision = "20261126_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "process_definitions",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("tenant_id", sa.String(100), nullable=False),
        sa.Column("company_id", sa.String(100), nullable=False),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("status", sa.String(30), nullable=False),
        sa.Column("current_version", sa.Integer(), nullable=False),
        sa.Column("created_by", sa.String(100), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_index(
        "ix_process_definitions_tenant",
        "process_definitions",
        ["tenant_id"],
    )
    op.create_index(
        "ix_process_definitions_status",
        "process_definitions",
        ["status"],
    )

    op.create_table(
        "process_versions",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "definition_id",
            sa.String(36),
            sa.ForeignKey(
                "process_definitions.id",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),
        sa.Column("version_number", sa.Integer(), nullable=False),
        sa.Column("steps", sa.JSON(), nullable=False),
        sa.Column("published", sa.Boolean(), nullable=False),
        sa.Column("created_by", sa.String(100), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.UniqueConstraint(
            "definition_id",
            "version_number",
            name="uq_process_definition_version",
        ),
    )

    op.create_index(
        "ix_process_versions_definition",
        "process_versions",
        ["definition_id"],
    )

    op.create_table(
        "process_executions",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "definition_id",
            sa.String(36),
            sa.ForeignKey("process_definitions.id"),
            nullable=False,
        ),
        sa.Column(
            "version_id",
            sa.String(36),
            sa.ForeignKey("process_versions.id"),
            nullable=False,
        ),
        sa.Column("tenant_id", sa.String(100), nullable=False),
        sa.Column("status", sa.String(30), nullable=False),
        sa.Column("variables", sa.JSON(), nullable=False),
        sa.Column("outputs", sa.JSON(), nullable=False),
        sa.Column("completed_steps", sa.JSON(), nullable=False),
        sa.Column("error", sa.Text(), nullable=True),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_index(
        "ix_process_executions_tenant",
        "process_executions",
        ["tenant_id"],
    )
    op.create_index(
        "ix_process_executions_status",
        "process_executions",
        ["status"],
    )
    op.create_index(
        "ix_process_executions_definition",
        "process_executions",
        ["definition_id"],
    )

    op.create_table(
        "process_approvals",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column(
            "execution_id",
            sa.String(36),
            sa.ForeignKey(
                "process_executions.id",
                ondelete="CASCADE",
            ),
            nullable=False,
        ),
        sa.Column("step_id", sa.String(100), nullable=False),
        sa.Column("status", sa.String(30), nullable=False),
        sa.Column("actor_id", sa.String(100), nullable=True),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("resolved_at", sa.DateTime(timezone=True), nullable=True),
        sa.UniqueConstraint(
            "execution_id",
            "step_id",
            name="uq_process_execution_step_approval",
        ),
    )

    op.create_index(
        "ix_process_approvals_status",
        "process_approvals",
        ["status"],
    )

    op.create_table(
        "process_audit_logs",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("tenant_id", sa.String(100), nullable=False),
        sa.Column(
            "definition_id",
            sa.String(36),
            sa.ForeignKey(
                "process_definitions.id",
                ondelete="SET NULL",
            ),
            nullable=True,
        ),
        sa.Column(
            "execution_id",
            sa.String(36),
            sa.ForeignKey(
                "process_executions.id",
                ondelete="SET NULL",
            ),
            nullable=True,
        ),
        sa.Column("actor_id", sa.String(100), nullable=False),
        sa.Column("action", sa.String(100), nullable=False),
        sa.Column("details", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_index(
        "ix_process_audit_tenant",
        "process_audit_logs",
        ["tenant_id"],
    )
    op.create_index(
        "ix_process_audit_execution",
        "process_audit_logs",
        ["execution_id"],
    )


def downgrade():
    op.drop_table("process_audit_logs")
    op.drop_table("process_approvals")
    op.drop_table("process_executions")
    op.drop_table("process_versions")
    op.drop_table("process_definitions")
