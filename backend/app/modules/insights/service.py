from collections import Counter, defaultdict
from decimal import Decimal
from statistics import median

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.process_automation.models import ProcessDefinition, ProcessExecution
from app.modules.insights.schemas import ForecastRequest, ReconciliationRequest


def forecast_trend(data: ForecastRequest) -> dict:
    values = data.historical_values
    count = len(values)
    mean_x = (count - 1) / 2
    mean_y = sum(values) / count
    denominator = sum((index - mean_x) ** 2 for index in range(count))
    slope = sum(
        (index - mean_x) * (value - mean_y)
        for index, value in enumerate(values)
    ) / denominator
    intercept = mean_y - slope * mean_x
    forecast_values = [
        round(intercept + slope * index, 4)
        for index in range(count, count + data.horizon)
    ]
    return {
        "series_name": data.series_name,
        "historical_count": count,
        "horizon": data.horizon,
        "method": "linear_trend_extrapolation",
        "trend_per_period": round(slope, 4),
        "forecast_values": forecast_values,
        "caveat": (
            "Trend extrapolation from supplied values only; not a causal model "
            "or a guarantee of future results."
        ),
    }


def reconcile(data: ReconciliationRequest) -> dict:
    statement_groups: dict[str, list] = defaultdict(list)
    ledger_groups: dict[str, list] = defaultdict(list)
    statement_totals: dict[str, Decimal] = defaultdict(Decimal)
    ledger_totals: dict[str, Decimal] = defaultdict(Decimal)

    for entry in data.statement:
        reference = entry.reference.strip().casefold()
        statement_groups[reference].append(entry)
        statement_totals[entry.currency] += entry.amount
    for entry in data.ledger:
        reference = entry.reference.strip().casefold()
        ledger_groups[reference].append(entry)
        ledger_totals[entry.currency] += entry.amount

    rows = []
    for reference in sorted(set(statement_groups) | set(ledger_groups)):
        statement_items = statement_groups[reference]
        ledger_items = ledger_groups[reference]
        statement = statement_items[0] if statement_items else None
        ledger = ledger_items[0] if ledger_items else None

        if len(statement_items) > 1 or len(ledger_items) > 1:
            row_status = "duplicate_reference"
        elif statement is None:
            row_status = "missing_from_statement"
        elif ledger is None:
            row_status = "missing_from_ledger"
        elif statement.currency != ledger.currency:
            row_status = "currency_mismatch"
        elif statement.amount != ledger.amount:
            row_status = "amount_mismatch"
        else:
            row_status = "matched"

        rows.append({
            "reference": statement.reference if statement else ledger.reference,
            "status": row_status,
            "statement_amount": statement.amount if statement else None,
            "ledger_amount": ledger.amount if ledger else None,
            "statement_currency": statement.currency if statement else None,
            "ledger_currency": ledger.currency if ledger else None,
            "statement_count": len(statement_items),
            "ledger_count": len(ledger_items),
        })

    matched_count = sum(row["status"] == "matched" for row in rows)
    totals_by_currency = {}
    for currency in sorted(set(statement_totals) | set(ledger_totals)):
        statement_total = statement_totals[currency]
        ledger_total = ledger_totals[currency]
        totals_by_currency[currency] = {
            "statement_total": round(statement_total, 4),
            "ledger_total": round(ledger_total, 4),
            "difference": round(statement_total - ledger_total, 4),
        }

    return {
        "matched_count": matched_count,
        "exception_count": len(rows) - matched_count,
        "rows": rows,
        "totals_by_currency": totals_by_currency,
    }


def process_mining(db: Session, tenant_id: str, limit: int = 1000) -> list[dict]:
    records = db.execute(
        select(ProcessExecution, ProcessDefinition.name)
        .join(ProcessDefinition, ProcessExecution.definition_id == ProcessDefinition.id)
        .where(ProcessExecution.tenant_id == tenant_id)
        .order_by(ProcessExecution.created_at.desc())
        .limit(limit)
    ).all()

    grouped: dict[str, dict] = {}
    for execution, process_name in records:
        group = grouped.setdefault(execution.definition_id, {
            "process_id": execution.definition_id,
            "process_name": process_name,
            "run_count": 0,
            "status_counts": Counter(),
            "durations": [],
        })
        group["run_count"] += 1
        group["status_counts"][execution.status] += 1
        if (
            execution.started_at is not None
            and execution.completed_at is not None
            and execution.completed_at >= execution.started_at
        ):
            group["durations"].append(
                (execution.completed_at - execution.started_at).total_seconds()
            )

    summaries = []
    for group in grouped.values():
        durations = group["durations"]
        statuses = dict(group["status_counts"])
        summaries.append({
            "process_id": group["process_id"],
            "process_name": group["process_name"],
            "run_count": group["run_count"],
            "status_counts": statuses,
            "completed_runs": statuses.get("completed", 0),
            "failed_runs": statuses.get("failed", 0),
            "average_cycle_time_seconds": (
                round(sum(durations) / len(durations), 3) if durations else None
            ),
            "median_cycle_time_seconds": (
                round(median(durations), 3) if durations else None
            ),
            "duration_sample_count": len(durations),
        })
    return sorted(summaries, key=lambda item: item["process_name"].casefold())
