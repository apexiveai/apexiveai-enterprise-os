from collections import Counter, deque
from threading import Lock
from time import perf_counter
from uuid import uuid4

from fastapi import Request


_traces: deque[dict] = deque(maxlen=1000)
_lock = Lock()


async def request_observability_middleware(request: Request, call_next):
    request_id = str(uuid4())
    started = perf_counter()
    trace = {
        "request_id": request_id,
        "method": request.method,
        "path": request.url.path,
        "status_code": None,
        "latency_ms": 0.0,
    }
    with _lock:
        _traces.append(trace)

    status_code = 500
    try:
        response = await call_next(request)
        status_code = response.status_code
        response.headers["X-Request-ID"] = request_id
        return response
    finally:
        with _lock:
            trace["status_code"] = status_code
            trace["latency_ms"] = round((perf_counter() - started) * 1000, 3)


def observability_snapshot() -> dict:
    with _lock:
        traces = list(_traces)
    latencies = sorted(trace["latency_ms"] for trace in traces)
    codes = Counter(
        str(trace["status_code"]) if trace["status_code"] is not None else "pending"
        for trace in traces
    )
    p95_index = max(0, math_ceil(len(latencies) * 0.95) - 1)
    return {
        "window_size": _traces.maxlen or 0,
        "request_count": len(traces),
        "error_count": sum(
            isinstance(trace["status_code"], int) and trace["status_code"] >= 500
            for trace in traces
        ),
        "average_latency_ms": round(sum(latencies) / len(latencies), 3) if latencies else 0.0,
        "p95_latency_ms": latencies[p95_index] if latencies else 0.0,
        "status_codes": dict(codes),
        "recent_traces": traces[-50:],
    }


def math_ceil(value: float) -> int:
    integer = int(value)
    return integer if integer == value else integer + 1
