from contextlib import asynccontextmanager
import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.v1.health import router as health_router
from app.db.base import Base
from app.db.session import close_connections, engine
from app.modules.workflow.routes import router as workflow_router
from app.modules.enterprise_suites import router as enterprise_suites_router
from app.modules.industrial.routes import router as industrial_router
from app.modules.industrial import models as industrial_models
from app.modules.process_automation import models as process_automation_models
from app.modules.process_automation.routes import router as process_automation_router
from app.modules.agents import models as agent_models
from app.modules.agents.routes import router as agents_router
from app.modules.platform import models as platform_models
from app.modules.platform.observability import request_observability_middleware
from app.modules.platform.routes import router as platform_router
from app.modules.insights.routes import router as insights_router
from app.modules.industry_solutions import models as industry_solution_models
from app.modules.industry_solutions.routes import router as industry_solutions_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    if settings.auto_create_tables:
        Base.metadata.create_all(bind=engine)
    yield
    close_connections()


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Enterprise AI Operating System",
    docs_url="/docs" if settings.environment.lower() != "production" else None,
    redoc_url="/redoc" if settings.environment.lower() != "production" else None,
    openapi_url="/openapi.json" if settings.environment.lower() != "production" else None,
    lifespan=lifespan,
)

cors_origins = [
    origin.strip().rstrip("/")
    for origin in settings.cors_origins.split(",")
    if origin.strip()
]
if cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
app.middleware("http")(request_observability_middleware)

frontend_directory_value = os.environ.get("APEXIVE_FRONTEND_DIR")
frontend_directory = Path(frontend_directory_value) if frontend_directory_value else None


@app.get("/", tags=["Root"])
def root():
    if frontend_directory:
        return FileResponse(frontend_directory / "index.html")
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
app.include_router(industrial_router, prefix="/api/v1")
app.include_router(process_automation_router, prefix="/api/v1")
app.include_router(agents_router, prefix="/api/v1")
app.include_router(platform_router, prefix="/api/v1")
app.include_router(insights_router, prefix="/api/v1")
app.include_router(industry_solutions_router, prefix="/api/v1")

if frontend_directory:
    app.mount("/", StaticFiles(directory=frontend_directory, html=True), name="frontend")
