
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.db.session import check_database, check_redis


router = APIRouter(tags=["Health"])


@router.get("/health/ready")
def readiness_check():

    database_status = check_database()
    redis_status = check_redis()

    ready = database_status and redis_status is not False

    response = {
        "status": "ready" if ready else "not_ready",
        "application": settings.app_name,
        "version": settings.app_version,
        "services": {
            "database": (
                "connected" if database_status else "disconnected"
            ),
            "redis": (
                "connected"
                if redis_status is True
                else "disconnected"
                if redis_status is False
                else "disabled"
            ),
        },
    }

    return JSONResponse(
        status_code=200 if ready else 503,
        content=response,
    )
