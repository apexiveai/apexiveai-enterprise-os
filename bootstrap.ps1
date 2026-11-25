
#!/usr/bin/env bash
set -euo pipefail

PROJECT="MAX-ENTERPRISE-OS"

mkdir -p "$PROJECT"
cd "$PROJECT"

# Backend structure
mkdir -p backend/app/{core,api/v1,models,schemas,services,modules/{identity,organization,finance,hr,procurement,inventory,workflow}}
mkdir -p backend/tests
mkdir -p database/{migrations,seeds}
mkdir -p infrastructure security documentation/{architecture,api,database,user-guides}
mkdir -p deployment ai-engine rpa-engine integrations

# Python dependencies
cat > backend/pyproject.toml <<'EOF'
[project]
name = "max-enterprise-os"
version = "0.1.0"
description = "MAX Myanmar Enterprise Operating System"
requires-python = ">=3.12"
dependencies = [
  "fastapi>=0.115,<1.0",
  "uvicorn[standard]>=0.30,<1.0",
  "pydantic-settings>=2.5,<3.0",
  "sqlalchemy[asyncio]>=2.0,<3.0",
  "asyncpg>=0.29,<1.0",
  "alembic>=1.13,<2.0",
  "redis>=5.0,<7.0",
]

[project.optional-dependencies]
dev = [
  "pytest>=8.0",
  "pytest-asyncio>=0.24",
  "httpx>=0.27",
  "ruff>=0.8",
]

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]

[tool.ruff]
line-length = 100
target-version = "py312"
EOF

# Configuration
cat > backend/app/core/config.py <<'EOF'
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "MAX ENTERPRISE OS"
    APP_VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"
    API_V1_PREFIX: str = "/api/v1"
    DATABASE_URL: str = "postgresql+asyncpg://max:max_dev_password@localhost:5432/max_enterprise"
    REDIS_URL: str = "redis://localhost:6379/0"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

settings = Settings()
EOF

# API health endpoint
cat > backend/app/api/v1/health.py <<'EOF'
from fastapi import APIRouter

router = APIRouter(tags=["System"])

@router.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "MAX ENTERPRISE OS",
        "version": "0.1.0",
    }
EOF

# Main application
cat > backend/app/main.py <<'EOF'
from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.health import router as health_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="MAX Myanmar Unified Enterprise Platform",
)

app.include_router(
    health_router,
    prefix=settings.API_V1_PREFIX,
)

@app.get("/")
async def root():
    return {
        "application": settings.APP_NAME,
        "status": "running",
        "api_docs": "/docs",
    }
EOF

touch backend/app/__init__.py
touch backend/app/core/__init__.py
touch backend/app/api/__init__.py
touch backend/app/api/v1/__init__.py

# Initial test
cat > backend/tests/test_health.py <<'EOF'
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
EOF

# Docker infrastructure
cat > docker-compose.yml <<'EOF'
services:
  postgres:
    image: postgres:17
    restart: unless-stopped
    environment:
      POSTGRES_DB: max_enterprise
      POSTGRES_USER: max
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:?Set POSTGRES_PASSWORD}
    ports:
      - "127.0.0.1:5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U max -d max_enterprise"]
      interval: 10s
      timeout: 5s
      retries: 5

  redis:
    image: redis:7-alpine
    restart: unless-stopped
    ports:
      - "127.0.0.1:6379:6379"
    volumes:
      - redis_data:/data
    command: redis-server --appendonly yes

volumes:
  postgres_data:
  redis_data:
EOF

# Environment template
cat > .env.example <<'EOF'
APP_NAME=MAX ENTERPRISE OS
ENVIRONMENT=development
POSTGRES_PASSWORD=change_this_local_password
DATABASE_URL=postgresql+asyncpg://max:change_this_local_password@localhost:5432/max_enterprise
REDIS_URL=redis://localhost:6379/0
EOF

cat > .gitignore <<'EOF'
.env
.venv/
__pycache__/
.pytest_cache/
.ruff_cache/
node_modules/
.next/
dist/
build/
*.pyc
EOF

cat > README.md <<'EOF'
# MAX ENTERPRISE OS

A unified enterprise operating system for MAX Myanmar.

## Architecture
- Frontend: Next.js + TypeScript
- Backend: FastAPI + Python
- Database: PostgreSQL
- Cache: Redis
- Architecture: Modular Monolith

## Backend Setup

cd backend
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
uvicorn app.main:app --reload

## API Documentation
http://localhost:8000/docs

## Infrastructure

Copy .env.example to .env and configure credentials.

docker compose up -d
EOF

echo "MAX ENTERPRISE OS foundation created."
