"""Main API Router aggregating sub-routers."""

from fastapi import APIRouter
from backend.api.v1 import health, sessions, state, predictions, models, batch
from backend.api.ws import stream

api_router = APIRouter()

api_router.include_router(health.router)
api_router.include_router(sessions.router)
api_router.include_router(state.router)
api_router.include_router(predictions.router)
api_router.include_router(models.router)
api_router.include_router(batch.router)
api_router.include_router(stream.router)
