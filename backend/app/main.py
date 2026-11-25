from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.config import settings
from app.api.v1.health import router as health_router
from app.db.session import close_connections
from app.modules.workflow.routes import router as workflow_router
from app.modules.enterprise_suites import router as enterprise_suites_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    close_connections()


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Enterprise AI Operating System",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)


@app.get("/", tags=["Root"])
def root():
    return {
        "application": settings.app_name,
        "version": settings.app_version,
        "status": "running",
    }


@app.get("/health", tags=["Health"])
def health():
    return {
        "status": "healthy",
        "application": settings.app_name,
        "version": settings.app_version,
    }


app.include_router(health_router)
app.include_router(workflow_router, prefix="/api/v1")
app.include_router(enterprise_suites_router, prefix="/api/v1")
