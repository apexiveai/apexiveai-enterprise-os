import math
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class ForecastRequest(StrictModel):
    series_name: str = Field(min_length=1, max_length=100)
    historical_values: list[float] = Field(min_length=3, max_length=120)
    horizon: int = Field(default=3, ge=1, le=24)

    @field_validator("historical_values")
    @classmethod
    def values_must_be_finite(cls, values: list[float]) -> list[float]:
        if any(not math.isfinite(value) for value in values):
            raise ValueError("Historical values must be finite numbers.")
        return values


class ReconciliationEntry(StrictModel):
    reference: str = Field(min_length=1, max_length=120)
    amount: Decimal = Field(max_digits=18, decimal_places=4)
    currency: str = Field(pattern=r"^[A-Z]{3}$")

    @field_validator("reference")
    @classmethod
    def reference_must_not_be_blank(cls, reference: str) -> str:
        normalized = reference.strip()
        if not normalized:
            raise ValueError("Reference must contain non-whitespace characters.")
        return normalized

    @field_validator("amount")
    @classmethod
    def amount_must_be_finite(cls, amount: Decimal) -> Decimal:
        if not amount.is_finite():
            raise ValueError("Amounts must be finite numbers.")
        return amount


class ReconciliationRequest(StrictModel):
    statement: list[ReconciliationEntry] = Field(min_length=1, max_length=5000)
    ledger: list[ReconciliationEntry] = Field(min_length=1, max_length=5000)


class ReconciliationRow(StrictModel):
    reference: str
    status: Literal[
        "matched",
        "amount_mismatch",
        "currency_mismatch",
        "missing_from_ledger",
        "missing_from_statement",
        "duplicate_reference",
    ]
    statement_amount: Decimal | None
    ledger_amount: Decimal | None
    statement_currency: str | None
    ledger_currency: str | None
    statement_count: int
    ledger_count: int


class ProcessMiningSummary(StrictModel):
    process_id: str
    process_name: str
    run_count: int
    status_counts: dict[str, int]
    completed_runs: int
    failed_runs: int
    average_cycle_time_seconds: float | None
    median_cycle_time_seconds: float | None
    duration_sample_count: int


class ForecastRead(StrictModel):
    series_name: str
    historical_count: int
    horizon: int
    method: Literal["linear_trend_extrapolation"]
    trend_per_period: float
    forecast_values: list[float]
    caveat: str


class CurrencyReconciliationTotal(StrictModel):
    statement_total: Decimal
    ledger_total: Decimal
    difference: Decimal


class ReconciliationRead(StrictModel):
    matched_count: int
    exception_count: int
    rows: list[ReconciliationRow]
    totals_by_currency: dict[str, CurrencyReconciliationTotal]
