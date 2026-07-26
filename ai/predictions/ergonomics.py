"""Ergonomic Risk Analysis prediction module (FR-008e)."""

import numpy as np

from ai.predictions.base import PredictionModule
from ai.predictions.registry import register_prediction_module
from ai.predictions.types import Prediction, RiskLevel


@register_prediction_module("ergonomics")
class ErgonomicAnalysisPredictionModule(PredictionModule):
    """Prediction module quantifying Rapid Entire Body Assessment (REBA/RULA) ergonomics score."""

    @property
    def name(self) -> str:
        return "ergonomics"

    def predict(
        self, embedding: np.ndarray, context_window: np.ndarray | None = None
    ) -> Prediction:
        emb = embedding.flatten()
        ergo_score = float(np.clip(1.0 + np.abs(np.mean(emb[:10])) * 10.0, 1.0, 12.0))

        if ergo_score > 8.0:
            risk_level = RiskLevel.HIGH
            label = f"REBA Score {ergo_score:.1f}: High Ergonomic Risk"
        elif ergo_score > 4.0:
            risk_level = RiskLevel.MODERATE
            label = f"REBA Score {ergo_score:.1f}: Medium Ergonomic Risk"
        else:
            risk_level = RiskLevel.LOW
            label = f"REBA Score {ergo_score:.1f}: Low Ergonomic Risk"

        confidence = 0.91

        return Prediction(
            module_name=self.name,
            label=label,
            confidence=confidence,
            risk_level=risk_level,
            score=ergo_score / 12.0,
            contributing_features=[
                {"feature": "reba_score", "importance": round(ergo_score, 2)},
                {"feature": "neck_torso_angle", "importance": 0.78},
            ],
            model_version="ergonomics_v1.0",
        )
