"""SDK data models for HumanOS Python SDK."""

from dataclasses import dataclass, field
from typing import Any


@dataclass
class SDKPrediction:
    """SDK Prediction object representation."""

    module_name: str
    label: str
    confidence: float
    risk_level: str
    score: float
    contributing_features: list[dict[str, Any]]
    timestamp: str
    model_version: str


@dataclass
class SDKHumanState:
    """SDK HumanState object representation."""

    session_id: str
    timestamp: str
    has_pose: bool
    posture_quality: float
    gait_stability: float
    fatigue_score: float
    predictions: list[SDKPrediction]


@dataclass
class SessionInfo:
    """SDK Session Info representation."""

    session_id: str
    camera_id: str
    status: str
    created_at: str
