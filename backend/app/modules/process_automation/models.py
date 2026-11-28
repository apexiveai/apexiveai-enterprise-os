from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import (
    DateTime, ForeignKey, Index, Integer, JSON,
    String, Text, UniqueConstraint
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


def utc_now():
    return datetime.now(timezone.utc)


class ProcessDefinition(Base):
    __tablename__ = "process_definitions"

    __table_args__ = (
        Index("ix_process_definitions_tenant", "tenant_id"),
        Index("ix_process_definitions_status", "status"),
    )

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    tenant_id: Mapped[str] = mapped_column(String(100), nullable=False)
    company_id: Mapped[str] = mapped_column(String(100), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="", nullable=False)
    status: Mapped[str] = mapped_column(
        String(30), default="draft", nullable=False
    )
    current_version: Mapped[int] = mapped_column(
        Integer, default=1, nullable=False
    )
    created_by: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now,
        onupdate=utc_now, nullable=False
    )


class ProcessVersion(Base):
    __tablename__ = "process_versions"

    __table_args__ = (
        UniqueConstraint(
            "definition_id", "version_number",
            name="uq_process_definition_version"
        ),
        Index("ix_process_versions_definition", "definition_id"),
    )

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    definition_id: Mapped[str] = mapped_column(
        ForeignKey("process_definitions.id", ondelete="CASCADE"),
        nullable=False
    )
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    steps: Mapped[list] = mapped_column(JSON, nullable=False)
    published: Mapped[bool] = mapped_column(
        default=False, nullable=False
    )
    created_by: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )


class ProcessExecution(Base):
    __tablename__ = "process_executions"

    __table_args__ = (
        Index("ix_process_executions_tenant", "tenant_id"),
        Index("ix_process_executions_status", "status"),
        Index("ix_process_executions_definition", "definition_id"),
    )

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    definition_id: Mapped[str] = mapped_column(
        ForeignKey("process_definitions.id"), nullable=False
    )
    version_id: Mapped[str] = mapped_column(
        ForeignKey("process_versions.id"), nullable=False
    )
    tenant_id: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(
        String(30), default="queued", nullable=False
    )
    variables: Mapped[dict] = mapped_column(
        JSON, default=dict, nullable=False
    )
    outputs: Mapped[dict] = mapped_column(
        JSON, default=dict, nullable=False
    )
    completed_steps: Mapped[list] = mapped_column(
        JSON, default=list, nullable=False
    )
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )


class ProcessApproval(Base):
    __tablename__ = "process_approvals"

    __table_args__ = (
        UniqueConstraint(
            "execution_id", "step_id",
            name="uq_process_execution_step_approval"
        ),
        Index("ix_process_approvals_status", "status"),
    )

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    execution_id: Mapped[str] = mapped_column(
        ForeignKey("process_executions.id", ondelete="CASCADE"),
        nullable=False
    )
    step_id: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(
        String(30), default="pending", nullable=False
    )
    actor_id: Mapped[str | None] = mapped_column(
        String(100), nullable=True
    )
    reason: Mapped[str] = mapped_column(Text, default="", nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
    resolved_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )


class ProcessAuditLog(Base):
    __tablename__ = "process_audit_logs"

    __table_args__ = (
        Index("ix_process_audit_tenant", "tenant_id"),
        Index("ix_process_audit_execution", "execution_id"),
    )

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )
    tenant_id: Mapped[str] = mapped_column(String(100), nullable=False)
    definition_id: Mapped[str | None] = mapped_column(
        ForeignKey("process_definitions.id", ondelete="SET NULL"),
        nullable=True
    )
    execution_id: Mapped[str | None] = mapped_column(
        ForeignKey("process_executions.id", ondelete="SET NULL"),
        nullable=True
    )
    actor_id: Mapped[str] = mapped_column(String(100), nullable=False)
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    details: Mapped[dict] = mapped_column(
        JSON, default=dict, nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now, nullable=False
    )
