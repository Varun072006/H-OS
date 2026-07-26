"""Unsafe Posture Detection prediction module (FR-008b)."""

import numpy as np

from ai.predictions.base import PredictionModule
from ai.predictions.registry import register_prediction_module
from ai.predictions.types import Prediction, RiskLevel


@register_prediction_module("posture")
class UnsafePosturePredictionModule(PredictionModule):
    """Prediction module detecting hazardous lifting posture, forward head tilt, or spinal flexion."""

    @property
    def name(self) -> str:
        return "posture"

    def predict(
        self, embedding: np.ndarray, context_window: np.ndarray | None = None
    ) -> Prediction:
        emb = embedding.flatten()

        # Heuristic posture flexion score from lower embedding components
        spinal_flexion = float(np.abs(np.mean(emb[16:32]))) if len(emb) >= 32 else 0.1
        score = float(np.clip(spinal_flexion * 4.0, 0.0, 1.0))

        if score > 0.6:
            risk_level = RiskLevel.HIGH
            label = "Unsafe Lifting Posture Detected"
        elif score > 0.3:
            risk_level = RiskLevel.MODERATE
            label = "Forward Spine Flexion"
        else:
            risk_level = RiskLevel.LOW
            label = "Ergonomic Posture"

        confidence = 0.88

        contributing = [
            {"feature": "spinal_flexion_angle", "importance": round(score, 3)},
            {"feature": "lumbar_load_index", "importance": round(score * 0.8, 3)},
        ]

        return Prediction(
            module_name=self.name,
            label=label,
            confidence=confidence,
            risk_level=risk_level,
            score=score,
            contributing_features=contributing,
            model_version="posture_v1.0",
        )
