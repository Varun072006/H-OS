"""Confidence score decomposition and calibration utilities."""


def decompose_confidence_score(
    raw_confidence: float, data_quality: float = 1.0, tracking_stability: float = 1.0
) -> dict[str, float]:
    """Decompose confidence score into model confidence, data quality, and tracking stability factors.

    Args:
        raw_confidence: Model raw confidence output.
        data_quality: Input landmark visibility/quality score [0.0, 1.0].
        tracking_stability: Temporal tracking stability factor [0.0, 1.0].

    Returns:
        Decomposed confidence dictionary.
    """
    calibrated = float(min(0.99, max(0.01, raw_confidence * data_quality * tracking_stability)))
    return {
        "calibrated_confidence": round(calibrated, 4),
        "model_raw_confidence": round(raw_confidence, 4),
        "data_quality_factor": round(data_quality, 4),
        "tracking_stability_factor": round(tracking_stability, 4),
    }
