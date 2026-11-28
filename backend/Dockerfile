
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PORT=8765 \
    ENVIRONMENT=production \
    OBJECT_STORAGE_PATH=/app/data/objects

WORKDIR /app/backend

RUN groupadd --system --gid 10001 appuser && \
    useradd --system --uid 10001 --gid appuser --create-home appuser

COPY requirements.txt ./requirements.txt
RUN python -m pip install --no-cache-dir --retries 5 --timeout 120 -r requirements.txt
COPY --chown=appuser:appuser . ./

# Runtime directories
RUN mkdir -p /app/data/objects && \
    chown appuser:appuser /app/data /app/data/objects

USER appuser

EXPOSE 8765

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import os, urllib.request; urllib.request.urlopen('http://127.0.0.1:' + os.getenv('PORT', '8765') + '/health/ready', timeout=5)" || exit 1

CMD ["sh", "-c", "exec uvicorn app.main:app --host 0.0.0.0 --port \"${PORT:-8765}\""]
