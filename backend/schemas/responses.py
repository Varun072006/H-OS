"""Pydantic response schemas for FastAPI endpoints."""

from datetime import datetime, timezone
from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Response payload for health check endpoint."""

    status: str = "ok"
    version: str = "0.1.0"
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class SessionResponse(BaseModel):
    """Response payload for camera session operations."""

    session_id: str
    camera_id: str
    status: str = "active"
    created_at: str


class PredictionItemSchema(BaseModel):
    """Single prediction result item schema."""

    module_name: str
    label: str
    confidence: float
    risk_level: str
    score: float
    contributing_features: list[dict]
    timestamp: str
    model_version: str


class HumanStateResponse(BaseModel):
    """Response payload representing current continuous human state."""

    session_id: str
    timestamp: str
    has_pose: bool
    posture_quality: float
    gait_stability: float
    fatigue_score: float
    predictions: list[PredictionItemSchema]
