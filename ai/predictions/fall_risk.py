"""Fall Risk Estimation prediction module (FR-008a)."""

import numpy as np

from ai.embeddings.analysis import compute_embedding_drift
from ai.predictions.base import PredictionModule
from ai.predictions.registry import register_prediction_module
from ai.predictions.types import Prediction, RiskLevel


@register_prediction_module("fall_risk")
class FallRiskPredictionModule(PredictionModule):
    """Prediction module for estimating real-time fall risk probability and instability trends."""

    @property
    def name(self) -> str:
        return "fall_risk"

    def predict(
        self, embedding: np.ndarray, context_window: np.ndarray | None = None
    ) -> Prediction:
        """Estimate fall risk score and categorical risk level from motion embedding and context."""
        emb = embedding.flatten()
        drift = compute_embedding_drift(context_window) if context_window is not None else 0.0

        # Calculate heuristic risk score based on motion feature magnitude & drift
        feature_std = float(np.std(emb[:16]))
        raw_score = float(np.clip(feature_std * 2.0 + drift * 1.5, 0.0, 1.0))

        if raw_score > 0.75:
            risk_level = RiskLevel.CRITICAL
            label = "Fall Risk Critical"
        elif raw_score > 0.5:
            risk_level = RiskLevel.HIGH
            label = "Fall Risk Elevated"
        elif raw_score > 0.25:
            risk_level = RiskLevel.MODERATE
            label = "Gait Instability Detected"
        else:
            risk_level = RiskLevel.LOW
            label = "Normal Mobility"

        confidence = min(0.95, 0.6 + raw_score * 0.35)

        contributing = [
            {"feature": "gait_instability", "importance": round(raw_score * 0.5, 3)},
            {"feature": "embedding_drift", "importance": round(drift * 0.5, 3)},
        ]

        return Prediction(
            module_name=self.name,
            label=label,
            confidence=confidence,
            risk_level=risk_level,
            score=raw_score,
            contributing_features=contributing,
            model_version="fall_risk_v1.0",
        )
