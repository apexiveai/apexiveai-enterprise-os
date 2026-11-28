from datetime import date
from decimal import Decimal, InvalidOperation

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.agents.models import AgentAuditLog
from app.modules.industry_solutions.models import IndustrySolutionRecord, utc_now
from app.modules.industry_solutions.schemas import (
    IndustryRecordCreate,
    IndustryRecordStatus,
)


SOLUTION_REQUIRED_FIELDS: dict[str, set[str]] = {
    "construction": {"site", "project_manager", "target_date", "budget"},
    "manufacturing": {"production_line", "sku", "quantity", "due_date"},
    "energy": {"asset", "site", "report_date", "reading", "unit"},
    "trading": {"customer", "product", "opportunity_value", "follow_up_date"},
    "hotels": {"guest", "room_type", "check_in", "check_out"},
    "agro": {"farm", "crop", "operation", "planned_date", "area"},
    "highway": {"station", "lane", "shift_date", "transaction_count", "collection_amount"},
    "logistics": {"shipment_ref", "customer", "origin", "destination", "delivery_due"},
}
SOLUTION_DATE_FIELDS: dict[str, set[str]] = {
    "construction": {"target_date"},
    "manufacturing": {"due_date"},
    "energy": {"report_date"},
    "trading": {"follow_up_date"},
    "hotels": {"check_in", "check_out"},
    "agro": {"planned_date"},
    "highway": {"shift_date"},
    "logistics": {"delivery_due"},
}
NUMERIC_FIELDS = {
    "budget",
    "quantity",
    "reading",
    "opportunity_value",
    "area",
    "transaction_count",
    "collection_amount",
}
INTEGER_FIELDS = {"quantity", "transaction_count"}


class IndustrySolutionInputError(Exception):
    pass


class IndustrySolutionRecordNotFoundError(Exception):
    pass


def _validate_payload(solution_key: str, payload: dict[str, str]) -> None:
    for field in SOLUTION_DATE_FIELDS[solution_key]:
        try:
            date.fromisoformat(payload[field])
        except ValueError as exc:
            raise IndustrySolutionInputError(f"{field} must be a valid ISO date.") from exc

    for field in NUMERIC_FIELDS.intersection(payload):
        try:
            number = Decimal(payload[field])
        except InvalidOperation as exc:
            raise IndustrySolutionInputError(f"{field} must be a valid number.") from exc
        if not number.is_finite() or number < 0:
            raise IndustrySolutionInputError(f"{field} must be a non-negative finite number.")
        if field in INTEGER_FIELDS and number != number.to_integral_value():
            raise IndustrySolutionInputError(f"{field} must be a whole number.")

    if solution_key == "hotels":
        if date.fromisoformat(payload["check_out"]) <= date.fromisoformat(payload["check_in"]):
            raise IndustrySolutionInputError("check_out must be after check_in.")


def list_records(
    db: Session,
    tenant_id: str,
    solution_key: str,
    status: IndustryRecordStatus | None,
    limit: int,
) -> list[IndustrySolutionRecord]:
    statement = select(IndustrySolutionRecord).where(
        IndustrySolutionRecord.tenant_id == tenant_id,
        IndustrySolutionRecord.solution_key == solution_key,
    )
    if status:
        statement = statement.where(IndustrySolutionRecord.status == status)
    statement = statement.order_by(
        IndustrySolutionRecord.updated_at.desc(),
        IndustrySolutionRecord.id,
    ).limit(limit)
    return list(db.scalars(statement).all())


def create_record(
    db: Session,
    solution_key: str,
    data: IndustryRecordCreate,
) -> IndustrySolutionRecord:
    required_fields = SOLUTION_REQUIRED_FIELDS[solution_key]
    supplied_fields = set(data.payload)
    missing_fields = required_fields - supplied_fields
    unexpected_fields = supplied_fields - required_fields
    if missing_fields:
        raise IndustrySolutionInputError(
            f"Missing required fields: {', '.join(sorted(missing_fields))}."
        )
    if unexpected_fields:
        raise IndustrySolutionInputError(
            f"Unsupported fields: {', '.join(sorted(unexpected_fields))}."
        )
    _validate_payload(solution_key, data.payload)

    record = IndustrySolutionRecord(
        tenant_id=data.tenant_id,
        solution_key=solution_key,
        title=data.title,
        status="open",
        payload=data.payload,
        created_by=data.actor_id,
    )
    db.add(record)
    db.flush()
    db.add(AgentAuditLog(
        tenant_id=data.tenant_id,
        actor_id=data.actor_id,
        action="industry_solution.record_created",
        resource_type="industry_solution_record",
        resource_id=record.id,
        details={"solution_key": solution_key, "title": record.title},
    ))
    db.commit()
    db.refresh(record)
    return record


def update_record_status(
    db: Session,
    tenant_id: str,
    solution_key: str,
    record_id: str,
    actor_id: str,
    status: IndustryRecordStatus,
) -> IndustrySolutionRecord:
    record = db.scalar(select(IndustrySolutionRecord).where(
        IndustrySolutionRecord.id == record_id,
        IndustrySolutionRecord.tenant_id == tenant_id,
        IndustrySolutionRecord.solution_key == solution_key,
    ))
    if record is None:
        raise IndustrySolutionRecordNotFoundError(record_id)

    previous_status = record.status
    record.status = status
    record.updated_at = utc_now()
    db.add(AgentAuditLog(
        tenant_id=tenant_id,
        actor_id=actor_id,
        action="industry_solution.record_status_updated",
        resource_type="industry_solution_record",
        resource_id=record.id,
        details={
            "solution_key": solution_key,
            "previous_status": previous_status,
            "status": status,
        },
    ))
    db.commit()
    db.refresh(record)
    return record
