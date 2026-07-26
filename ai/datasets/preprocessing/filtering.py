"""Joint coordinate temporal filtering and smoothing utilities."""

import numpy as np


def moving_average_smooth(tensor: np.ndarray, window_size: int = 3) -> np.ndarray:
    """Smooth joint trajectory across time steps using a moving average window.

    Args:
        tensor: Feature array (C, T, V).
        window_size: Odd integer window size for smoothing.

    Returns:
        Smoothed tensor array.
    """
    if window_size <= 1 or tensor.shape[1] < window_size:
        return tensor

    out = tensor.copy()
    c, t, v = out.shape
    half_w = window_size // 2

    for ch in range(min(c, 3)):
        for j in range(v):
            series = out[ch, :, j]
            padded = np.pad(series, (half_w, half_w), mode="edge")
            smoothed = np.convolve(padded, np.ones(window_size) / window_size, mode="valid")
            out[ch, :, j] = smoothed[:t]

    return out
