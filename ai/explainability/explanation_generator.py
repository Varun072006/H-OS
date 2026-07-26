"""Natural language explanation text generator for model predictions (FR-010)."""

from typing import Any


def generate_human_explanation(
    module_name: str,
    label: str,
    confidence: float,
    score: float,
    contributing_features: list[dict[str, Any]],
) -> str:
    """Generate human-readable, calibrated explanation text avoiding overstating predictions.

    Args:
        module_name: Name of prediction module (e.g. 'fall_risk', 'posture').
        label: Primary prediction label.
        confidence: Calibrated confidence score [0.0, 1.0].
        score: Continuous prediction score.
        contributing_features: List of feature attributions.

    Returns:
        Human-readable explanation string.
    """
    conf_str = "high" if confidence > 0.8 else ("moderate" if confidence > 0.5 else "low")

    top_feature_names = [f.get("feature", f"joint_{f.get('joint_index', 0)}") for f in contributing_features[:2]]
    features_str = " and ".join(top_feature_names) if top_feature_names else "overall motion pattern"

    if module_name == "fall_risk":
        return (
            f"Fall risk is assessed as '{label}' with {conf_str} confidence ({confidence*100:.0f}%). "
            f"Primary contributing factors are {features_str} over the observed temporal window."
        )
    elif module_name == "posture":
        return (
            f"Posture analysis indicates '{label}' with {conf_str} confidence ({confidence*100:.0f}%). "
            f"Observed spinal load index is {score:.2f}."
        )
    else:
        return (
            f"Model predicted '{label}' with {conf_str} confidence ({confidence*100:.0f}%) "
            f"based on {features_str}."
        )
