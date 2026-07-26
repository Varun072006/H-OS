"""Preprocessing utilities for missing joint coordinate interpolation."""

import numpy as np


def interpolate_missing_joints(tensor: np.ndarray, mask: np.ndarray | None = None) -> np.ndarray:
    """Interpolate missing/zero-confidence joint coordinates across time steps T.

    Args:
        tensor: Skeleton feature array of shape (C, T, V).
        mask: Optional boolean mask (T, V) where True indicates valid and False indicates missing.

    Returns:
        Tensor with missing values interpolated across neighboring frames.
    """
    out = tensor.copy()
    c, t, v = out.shape

    if mask is None:
        # Infer missing where all xyz channels are exactly 0.0
        mask = np.any(out[:3, :, :] != 0.0, axis=0)  # Shape (T, V)

    for j in range(v):
        valid_t = np.where(mask[:, j])[0]
        if len(valid_t) == 0 or len(valid_t) == t:
            continue

        for ch in range(min(c, 3)):
            vals = out[ch, valid_t, j]
            all_t = np.arange(t)
            out[ch, :, j] = np.interp(all_t, valid_t, vals)

    return out
