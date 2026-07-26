"""Model management endpoints."""

from fastapi import APIRouter
from backend.services.model_manager import ModelManager

router = APIRouter(prefix="/models", tags=["Models"])

_model_manager = ModelManager()


@router.get("")
async def list_models() -> list[dict]:
    """List registered AI models and versions."""
    return _model_manager.list_models()
