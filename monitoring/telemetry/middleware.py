"""FastAPI middleware tracking request latencies and HTTP status metrics."""

import time
from fastapi import Request
from monitoring.telemetry.metrics import API_REQUEST_LATENCY_MS


async def telemetry_middleware(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    elapsed_ms = (time.perf_counter() - start_time) * 1000.0

    API_REQUEST_LATENCY_MS.observe(elapsed_ms)
    response.headers["X-Response-Time-Ms"] = f"{elapsed_ms:.2f}"
    return response
