from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.modules.industrial.schemas import (
    DeviceCreate,
    DeviceRead,
    DeviceUpdate,
    DeviceStatusUpdate,
)
from app.modules.industrial.service import DeviceService, DeviceNotFoundError

router = APIRouter(prefix="/industrial", tags=["Industrial Integration"])


@router.get("/health")
def industrial_health():
    return {"module": "industrial-integration", "status": "ready"}


@router.post(
    "/devices",
    response_model=DeviceRead,
    status_code=status.HTTP_201_CREATED,
)
def create_device(data: DeviceCreate, db: Session = Depends(get_db)):
    return DeviceService.create(db, data)


@router.get("/devices", response_model=list[DeviceRead])
def list_devices(
    tenant_id: str = Query(min_length=1),
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return DeviceService.list(db, tenant_id, offset, limit)


@router.get("/devices/{device_id}", response_model=DeviceRead)
def get_device(
    device_id: str,
    tenant_id: str = Query(min_length=1),
    db: Session = Depends(get_db),
):
    try:
        return DeviceService.get(db, tenant_id, device_id)
    except DeviceNotFoundError:
        raise HTTPException(status_code=404, detail="Device not found")


@router.patch("/devices/{device_id}", response_model=DeviceRead)
def update_device(
    device_id: str,
    data: DeviceUpdate,
    tenant_id: str = Query(min_length=1),
    db: Session = Depends(get_db),
):
    try:
        device = DeviceService.get(db, tenant_id, device_id)
        return DeviceService.update(db, device, data)
    except DeviceNotFoundError:
        raise HTTPException(status_code=404, detail="Device not found")


@router.patch("/devices/{device_id}/status", response_model=DeviceRead)
def update_device_status(
    device_id: str,
    data: DeviceStatusUpdate,
    tenant_id: str = Query(min_length=1),
    db: Session = Depends(get_db),
):
    try:
        device = DeviceService.get(db, tenant_id, device_id)
        return DeviceService.set_status(db, device, data.status)
    except DeviceNotFoundError:
        raise HTTPException(status_code=404, detail="Device not found")


@router.delete(
    "/devices/{device_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def deactivate_device(
    device_id: str,
    tenant_id: str = Query(min_length=1),
    db: Session = Depends(get_db),
):
    try:
        device = DeviceService.get(db, tenant_id, device_id)
        DeviceService.deactivate(db, device)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except DeviceNotFoundError:
        raise HTTPException(status_code=404, detail="Device not found")
