"""Health check endpoints."""

from fastapi import APIRouter
from backend.schemas.responses import HealthResponse

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse)
async def get_health() -> HealthResponse:
    """Get system health status."""
    return HealthResponse()
