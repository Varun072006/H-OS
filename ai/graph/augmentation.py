"""Graph-level data augmentations for skeletal motion sequences."""

import numpy as np


def random_joint_jitter(
    tensor: np.ndarray, std: float = 0.01, p: float = 0.5
) -> np.ndarray:
    """Add Gaussian noise jittering to joint coordinates.

    Args:
        tensor: Array (C, T, V).
        std: Noise standard deviation.
        p: Probability of applying augmentation.

    Returns:
        Augmented feature tensor.
    """
    if np.random.rand() > p:
        return tensor

    out = tensor.copy()
    noise = np.random.normal(0, std, size=out[:3].shape).astype(np.float32)
    out[:3] += noise
    return out


def random_spatial_rotation(
    tensor: np.ndarray, max_degrees: float = 15.0, p: float = 0.5
) -> np.ndarray:
    """Apply random 3D rotation matrix to joint coordinates.

    Args:
        tensor: Array (C, T, V).
        max_degrees: Maximum rotation angle in degrees.
        p: Probability of applying augmentation.

    Returns:
        Rotated feature tensor.
    """
    if np.random.rand() > p:
        return tensor

    out = tensor.copy()
    rad = np.radians(np.random.uniform(-max_degrees, max_degrees))
    cos_a, sin_a = np.cos(rad), np.sin(rad)

    # 2D Z-axis rotation matrix
    rot_mat = np.array(
        [[cos_a, -sin_a, 0.0], [sin_a, cos_a, 0.0], [0.0, 0.0, 1.0]],
        dtype=np.float32,
    )

    # Reshape for matrix multiplication: (3, T*V) -> (3, T*V)
    c, t, v = out.shape
    coords_2d = out[:3].reshape(3, t * v)
    rotated_coords = rot_mat @ coords_2d
    out[:3] = rotated_coords.reshape(3, t, v)

    return out


def temporal_crop_or_pad(
    tensor: np.ndarray, target_frames: int
) -> np.ndarray:
    """Crop or pad temporal dimension T to target_frames length.

    Args:
        tensor: Array (C, T, V).
        target_frames: Desired temporal length T_target.

    Returns:
        Resampled tensor (C, target_frames, V).
    """
    c, t, v = tensor.shape
    if t == target_frames:
        return tensor

    if t > target_frames:
        # Uniform temporal sampling
        indices = np.linspace(0, t - 1, target_frames, dtype=int)
        return tensor[:, indices, :]
    else:
        # Zero padding in temporal dimension
        padded = np.zeros((c, target_frames, v), dtype=tensor.dtype)
        padded[:, :t, :] = tensor
        return padded
