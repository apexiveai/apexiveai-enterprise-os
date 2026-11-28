from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.modules.insights import service
from app.modules.insights.schemas import (
    ForecastRead,
    ForecastRequest,
    ProcessMiningSummary,
    ReconciliationRead,
    ReconciliationRequest,
)


router = APIRouter(prefix="/insights", tags=["Business Intelligence"])


@router.post("/forecast", response_model=ForecastRead)
def forecast(data: ForecastRequest):
    return service.forecast_trend(data)


@router.post("/reconciliation", response_model=ReconciliationRead)
def reconcile(data: ReconciliationRequest):
    return service.reconcile(data)


@router.get("/process-mining", response_model=list[ProcessMiningSummary])
def get_process_mining(
    tenant_id: str = Query(min_length=1, max_length=100),
    limit: int = Query(default=1000, ge=1, le=10000),
    db: Session = Depends(get_db),
):
    return service.process_mining(db, tenant_id, limit)
