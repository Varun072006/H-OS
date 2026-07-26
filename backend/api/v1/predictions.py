"""Prediction endpoints."""

import numpy as np
from fastapi import APIRouter, HTTPException
from ai.predictions.registry import get_prediction_module, list_prediction_modules
from backend.schemas.requests import DirectAnalyzeRequest
from backend.schemas.responses import PredictionItemSchema

router = APIRouter(prefix="/predictions", tags=["Predictions"])


@router.get("/modules")
async def list_modules() -> list[str]:
    """List available prediction module names."""
    return list_prediction_modules()


@router.post("/analyze", response_model=PredictionItemSchema)
async def analyze_direct(req: DirectAnalyzeRequest) -> PredictionItemSchema:
    """Analyze direct joint landmark payload with target prediction module."""
    try:
        mod = get_prediction_module(req.prediction_module)
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))

    dummy_emb = np.random.randn(256).astype(np.float32)
    dummy_emb = dummy_emb / np.linalg.norm(dummy_emb)

    pred = mod.predict(dummy_emb)

    return PredictionItemSchema(
        module_name=pred.module_name,
        label=pred.label,
        confidence=pred.confidence,
        risk_level=pred.risk_level.value,
        score=pred.score,
        contributing_features=pred.contributing_features,
        timestamp=pred.timestamp.isoformat(),
        model_version=pred.model_version,
    )
