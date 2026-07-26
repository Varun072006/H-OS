"""Joint and motion feature attribution for model explainability."""

import numpy as np


def compute_joint_importance(motion_tensor: np.ndarray) -> list[dict[str, float]]:
    """Compute joint motion variance importance attributions.

    Args:
        motion_tensor: Motion array of shape (C, T, V).

    Returns:
        List of dicts containing joint_index and relative importance score.
    """
    c, t, v = motion_tensor.shape
    if v == 0:
        return []

    # Calculate spatial variance per joint across time steps
    joint_variances = np.var(motion_tensor[:3, :, :], axis=(0, 1))  # Shape (V,)
    total_var = float(np.sum(joint_variances))
    if total_var < 1e-6:
        total_var = 1.0

    importance_scores = joint_variances / total_var

    results = []
    for j_idx in range(v):
        results.append(
            {
                "joint_index": j_idx,
                "importance": round(float(importance_scores[j_idx]), 4),
            }
        )

    # Sort descending by importance
    results.sort(key=lambda x: x["importance"], reverse=True)
    return results
