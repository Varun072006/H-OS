"""Prediction data structures, risk level enums, and prediction outputs."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class RiskLevel(str, Enum):
    """Categorical risk assessment level."""

    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    CRITICAL = "critical"
    UNKNOWN = "unknown"


@dataclass
class Prediction:
    """Standardized prediction output returned by any prediction module.

    Attributes:
        module_name: Name of prediction module (e.g. 'fall_risk', 'posture').
        label: Human-readable primary prediction label.
        confidence: Prediction confidence score [0.0, 1.0].
        risk_level: Categorical RiskLevel (low, moderate, high, critical).
        score: Continuous score or probability [0.0, 1.0].
        contributing_features: List of joint/movement feature attribution dicts.
        timestamp: Timestamp of prediction.
        model_version: Version identifier of underlying model.
        metadata: Extra contextual key-value details.
    """

    module_name: str
    label: str
    confidence: float
    risk_level: RiskLevel = RiskLevel.LOW
    score: float = 0.0
    contributing_features: list[dict[str, Any]] = field(default_factory=list)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    model_version: str = "v1.0.0"
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize prediction to dictionary representation."""
        return {
            "module_name": self.module_name,
            "label": self.label,
            "confidence": round(self.confidence, 4),
            "risk_level": self.risk_level.value,
            "score": round(self.score, 4),
            "contributing_features": self.contributing_features,
            "timestamp": self.timestamp.isoformat(),
            "model_version": self.model_version,
            "metadata": self.metadata,
        }
