from sqlalchemy import select
from sqlalchemy.orm import Session

from app.modules.industrial.models import IndustrialDevice
from app.modules.industrial.schemas import DeviceCreate, DeviceUpdate


class DeviceNotFoundError(Exception):
    pass


class DeviceService:

    @staticmethod
    def create(db: Session, data: DeviceCreate) -> IndustrialDevice:
        device = IndustrialDevice(**data.model_dump())
        db.add(device)
        db.commit()
        db.refresh(device)
        return device

    @staticmethod
    def list(
        db: Session, tenant_id: str, offset: int = 0, limit: int = 100
    ):
        statement = (
            select(IndustrialDevice)
            .where(IndustrialDevice.tenant_id == tenant_id)
            .order_by(IndustrialDevice.created_at.desc())
            .offset(offset)
            .limit(limit)
        )
        return list(db.scalars(statement).all())

    @staticmethod
    def get(db: Session, tenant_id: str, device_id: str):
        statement = select(IndustrialDevice).where(
            IndustrialDevice.id == device_id,
            IndustrialDevice.tenant_id == tenant_id,
        )
        device = db.scalar(statement)
        if device is None:
            raise DeviceNotFoundError(device_id)
        return device

    @staticmethod
    def update(db: Session, device, data: DeviceUpdate):
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(device, key, value)
        db.commit()
        db.refresh(device)
        return device

    @staticmethod
    def set_status(db: Session, device, status: str):
        device.status = status
        db.commit()
        db.refresh(device)
        return device

    @staticmethod
    def deactivate(db: Session, device):
        device.status = "disabled"
        db.commit()
