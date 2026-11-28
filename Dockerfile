FROM node:24-alpine AS frontend-build

ARG VITE_TENANT_ID=local-workspace
ENV VITE_TENANT_ID=${VITE_TENANT_ID}

WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

FROM python:3.12-slim AS application

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PORT=8765 \
    ENVIRONMENT=production

WORKDIR /app/backend

RUN groupadd --system --gid 10001 appuser && \
    useradd --system --uid 10001 --gid appuser --create-home appuser

COPY backend/requirements.txt ./requirements.txt
RUN python -m pip install --no-cache-dir --retries 5 --timeout 120 -r requirements.txt

COPY --chown=appuser:appuser backend/ ./
COPY --from=frontend-build --chown=appuser:appuser /app/frontend/dist /app/frontend/dist

RUN mkdir -p /app/data/objects && \
    chown appuser:appuser /app/data /app/data/objects

ENV APEXIVE_FRONTEND_DIR=/app/frontend/dist \
    OBJECT_STORAGE_PATH=/app/data/objects

USER appuser

EXPOSE 8765

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python -c "import os, urllib.request; urllib.request.urlopen('http://127.0.0.1:' + os.getenv('PORT', '8765') + '/health/ready', timeout=5)" || exit 1

CMD ["sh", "-c", "exec uvicorn app.main:app --host 0.0.0.0 --port \"${PORT:-8765}\""]
