"""Normalizations and coordinate transformations for motion graphs."""

import numpy as np


def normalize_motion_tensor(
    tensor: np.ndarray,
    center_joint_idx: int = 0,
    target_scale: float = 1.0,
) -> np.ndarray:
    """Normalize skeleton sequence feature tensor to origin-centered and scale-invariant coordinates.

    Args:
        tensor: Motion feature array of shape (C, T, V) or (N, C, T, V).
                C >= 3 (x, y, z, ...).
        center_joint_idx: Index of joint to set as origin (default: 0).
        target_scale: Scale target factor.

    Returns:
        Normalized tensor of same shape.
    """
    out = tensor.copy()
    is_4d = out.ndim == 4

    if not is_4d:
        out = out[np.newaxis, ...]  # Shape (1, C, T, V)

    # Shift origin to center_joint_idx across all time steps
    # center_coords shape: (N, 3, T, 1)
    center_coords = out[:, :3, :, center_joint_idx : center_joint_idx + 1]
    out[:, :3, :, :] -= center_coords

    # Compute bounding scale factor across all joints
    # max_dist shape: (N, 1, 1, 1)
    spatial_dist = np.linalg.norm(out[:, :3, :, :], axis=1, keepdims=True)  # (N, 1, T, V)
    max_dist = np.max(spatial_dist, axis=(2, 3), keepdims=True)  # (N, 1, 1, 1)
    max_dist = np.where(max_dist < 1e-6, 1.0, max_dist)

    out[:, :3, :, :] = (out[:, :3, :, :] / max_dist) * target_scale

    if not is_4d:
        out = out[0]

    return out
