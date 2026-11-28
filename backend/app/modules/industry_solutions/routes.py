from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.modules.industry_solutions import service
from app.modules.industry_solutions.schemas import (
    IndustryRecordCreate,
    IndustryRecordRead,
    IndustryRecordStatus,
    IndustryRecordStatusUpdate,
    IndustrySolutionKey,
)


router = APIRouter(prefix="/industry-solutions", tags=["Industry Solutions"])


@router.get("/{solution_key}/records", response_model=list[IndustryRecordRead])
def get_records(
    solution_key: IndustrySolutionKey,
    tenant_id: str = Query(min_length=1, max_length=100),
    record_status: IndustryRecordStatus | None = Query(default=None, alias="status"),
    limit: int = Query(default=200, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return service.list_records(db, tenant_id, solution_key, record_status, limit)


@router.post(
    "/{solution_key}/records",
    response_model=IndustryRecordRead,
    status_code=status.HTTP_201_CREATED,
)
def create_record(
    solution_key: IndustrySolutionKey,
    data: IndustryRecordCreate,
    db: Session = Depends(get_db),
):
    try:
        return service.create_record(db, solution_key, data)
    except service.IndustrySolutionInputError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.patch(
    "/{solution_key}/records/{record_id}",
    response_model=IndustryRecordRead,
)
def update_record_status(
    solution_key: IndustrySolutionKey,
    record_id: str,
    data: IndustryRecordStatusUpdate,
    db: Session = Depends(get_db),
):
    try:
        return service.update_record_status(
            db,
            data.tenant_id,
            solution_key,
            record_id,
            data.actor_id,
            data.status,
        )
    except service.IndustrySolutionRecordNotFoundError as exc:
        raise HTTPException(status_code=404, detail="Industry record not found.") from exc
