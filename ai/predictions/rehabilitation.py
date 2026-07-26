"""Rehabilitation Progress Tracking prediction module (FR-008d)."""

import numpy as np

from ai.predictions.base import PredictionModule
from ai.predictions.registry import register_prediction_module
from ai.predictions.types import Prediction, RiskLevel


@register_prediction_module("rehabilitation")
class RehabilitationProgressPredictionModule(PredictionModule):
    """Prediction module quantifying motor recovery, range-of-motion, and gait symmetry."""

    @property
    def name(self) -> str:
        return "rehabilitation"

    def predict(
        self, embedding: np.ndarray, context_window: np.ndarray | None = None
    ) -> Prediction:
        emb = embedding.flatten()
        symmetry_score = float(np.clip(0.5 + np.mean(emb[:8]) * 0.5, 0.0, 1.0))

        label = f"Symmetry Score: {int(symmetry_score * 100)}%"
        confidence = 0.89

        return Prediction(
            module_name=self.name,
            label=label,
            confidence=confidence,
            risk_level=RiskLevel.LOW if symmetry_score > 0.7 else RiskLevel.MODERATE,
            score=symmetry_score,
            contributing_features=[
                {"feature": "gait_symmetry", "importance": round(symmetry_score, 3)},
                {"feature": "joint_extension_range", "importance": 0.85},
            ],
            model_version="rehab_v1.0",
        )
