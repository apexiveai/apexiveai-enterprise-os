"""Add core intelligence infrastructure persistence.

Revision ID: 20261126_0003
Revises: 20261126_0002
"""

from alembic import op
import sqlalchemy as sa


revision = "20261126_0003"
down_revision = "20261126_0002"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "knowledge_documents",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("tenant_id", sa.String(100), nullable=False),
        sa.Column("title", sa.String(250), nullable=False),
        sa.Column("source", sa.String(500), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("vector", sa.JSON(), nullable=False),
        sa.Column("created_by", sa.String(100), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(
        "ix_knowledge_documents_tenant_created",
        "knowledge_documents",
        ["tenant_id", "created_at"],
    )

    op.create_table(
        "knowledge_relations",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("tenant_id", sa.String(100), nullable=False),
        sa.Column(
            "document_id",
            sa.String(36),
            sa.ForeignKey("knowledge_documents.id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column("subject", sa.String(200), nullable=False),
        sa.Column("predicate", sa.String(120), nullable=False),
        sa.Column("object", sa.String(200), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(
        "ix_knowledge_relations_tenant",
        "knowledge_relations",
        ["tenant_id"],
    )
    op.create_index(
        "ix_knowledge_relations_document",
        "knowledge_relations",
        ["document_id"],
    )

    op.create_table(
        "platform_events",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("tenant_id", sa.String(100), nullable=False),
        sa.Column("event_type", sa.String(160), nullable=False),
        sa.Column("payload", sa.JSON(), nullable=False),
        sa.Column("status", sa.String(20), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("acknowledged_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index(
        "ix_platform_events_tenant_status_created",
        "platform_events",
        ["tenant_id", "status", "created_at"],
    )

    op.create_table(
        "evaluation_runs",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("tenant_id", sa.String(100), nullable=False),
        sa.Column(
            "agent_id",
            sa.String(36),
            sa.ForeignKey("agent_definitions.id", ondelete="SET NULL"),
            nullable=True,
        ),
        sa.Column("prompt", sa.Text(), nullable=False),
        sa.Column("output", sa.Text(), nullable=False),
        sa.Column("required_checks", sa.JSON(), nullable=False),
        sa.Column("result", sa.JSON(), nullable=False),
        sa.Column("score", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(
        "ix_evaluation_runs_tenant_created",
        "evaluation_runs",
        ["tenant_id", "created_at"],
    )

    op.create_table(
        "stored_objects",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("tenant_id", sa.String(100), nullable=False),
        sa.Column("object_key", sa.String(80), nullable=False, unique=True),
        sa.Column("filename", sa.String(250), nullable=False),
        sa.Column("content_type", sa.String(120), nullable=False),
        sa.Column("size_bytes", sa.Integer(), nullable=False),
        sa.Column("created_by", sa.String(100), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    )
    op.create_index(
        "ix_stored_objects_tenant_created",
        "stored_objects",
        ["tenant_id", "created_at"],
    )


def downgrade():
    op.drop_table("stored_objects")
    op.drop_table("evaluation_runs")
    op.drop_table("platform_events")
    op.drop_table("knowledge_relations")
    op.drop_table("knowledge_documents")
