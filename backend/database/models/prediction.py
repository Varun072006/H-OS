"""Database prediction log record model."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class DBPredictionRecord:
    """Prediction log record representation for persistent storage."""

    id: str
    session_id: str
    module_name: str
    label: str
    confidence: float
    risk_level: str
    score: float
    contributing_features: list[dict[str, Any]]
    model_version: str
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
