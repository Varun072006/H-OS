"""Unit tests for Explainability & Reasoning engine (FR-010)."""

import numpy as np
import pytest

from ai.explainability.feature_attribution import compute_joint_importance
from ai.explainability.confidence_breakdown import decompose_confidence_score
from ai.explainability.explanation_generator import generate_human_explanation
from ai.predictions.types import Prediction, RiskLevel
from ai.reasoning.causal import CausalChain
from ai.reasoning.engine import ReasoningEngine


def test_feature_attribution_calculation() -> None:
    """Test computing joint feature importance scores."""
    motion_tensor = np.random.randn(4, 10, 33).astype(np.float32)
    attributions = compute_joint_importance(motion_tensor)

    assert len(attributions) == 33
    assert "joint_index" in attributions[0]
    assert "importance" in attributions[0]
    # Sum of importances should sum to ~1.0
    total = sum(item["importance"] for item in attributions)
    assert abs(total - 1.0) < 1e-3


def test_confidence_breakdown_decomposition() -> None:
    """Test decomposing confidence score."""
    decomp = decompose_confidence_score(raw_confidence=0.9, data_quality=0.8, tracking_stability=1.0)
    assert decomp["calibrated_confidence"] == 0.72
    assert decomp["model_raw_confidence"] == 0.9


def test_explanation_generator() -> None:
    """Test natural language explanation generator."""
    text = generate_human_explanation(
        module_name="fall_risk",
        label="Fall Risk Elevated",
        confidence=0.85,
        score=0.6,
        contributing_features=[{"feature": "gait_instability", "importance": 0.4}],
    )
    assert "Fall Risk Elevated" in text
    assert "gait_instability" in text


def test_reasoning_engine_eval() -> None:
    """Test ReasoningEngine generating causal recommendations."""
    engine = ReasoningEngine()
    pred = Prediction(
        module_name="fall_risk",
        label="Fall Risk Elevated",
        confidence=0.85,
        risk_level=RiskLevel.HIGH,
        score=0.6,
        contributing_features=[{"feature": "gait_instability", "importance": 0.6}],
    )

    chain = engine.evaluate_prediction(pred)
    assert isinstance(chain, CausalChain)
    assert "seated rest" in chain.recommendation
