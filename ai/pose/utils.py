"""Pose preprocessing, normalization, and mathematical utility functions."""

import numpy as np

from ai.pose.types import Joint, Skeleton

# MediaPipe 33 landmark names map
MEDIAPIPE_JOINT_NAMES = [
    "nose",
    "left_eye_inner",
    "left_eye",
    "left_eye_outer",
    "right_eye_inner",
    "right_eye",
    "right_eye_outer",
    "left_ear",
    "right_ear",
    "mouth_left",
    "mouth_right",
    "left_shoulder",
    "right_shoulder",
    "left_elbow",
    "right_elbow",
    "left_wrist",
    "right_wrist",
    "left_pinky",
    "right_pinky",
    "left_index",
    "right_index",
    "left_thumb",
    "right_thumb",
    "left_hip",
    "right_hip",
    "left_knee",
    "right_knee",
    "left_ankle",
    "right_ankle",
    "left_heel",
    "right_heel",
    "left_foot_index",
    "right_foot_index",
]


def calculate_center_of_mass(joints: list[Joint]) -> tuple[float, float, float]:
    """Calculate central body reference point (midpoint of hips or shoulders).

    Args:
        joints: List of Joint landmarks.

    Returns:
        (x, y, z) coordinates of center of mass.
    """
    if not joints:
        return (0.0, 0.0, 0.0)

    # Prefer hip midpoint if available (MediaPipe landmarks 23 and 24)
    hip_left = next((j for j in joints if j.name == "left_hip" or j.id == 23), None)
    hip_right = next((j for j in joints if j.name == "right_hip" or j.id == 24), None)

    if hip_left and hip_right:
        return (
            (hip_left.x + hip_right.x) / 2.0,
            (hip_left.y + hip_right.y) / 2.0,
            (hip_left.z + hip_right.z) / 2.0,
        )

    # Fallback to mean of all joint positions
    x_mean = float(np.mean([j.x for j in joints]))
    y_mean = float(np.mean([j.y for j in joints]))
    z_mean = float(np.mean([j.z for j in joints]))
    return (x_mean, y_mean, z_mean)


def normalize_skeleton(
    skeleton: Skeleton, target_scale: float = 1.0
) -> Skeleton:
    """Normalize skeleton coordinates to be body-centered (origin at hip center) and scale invariant.

    Args:
        skeleton: Input Skeleton object.
        target_scale: Desired bounding height scale.

    Returns:
        A new Skeleton object with normalized coordinates.
    """
    if not skeleton.joints:
        return skeleton

    cx, cy, cz = calculate_center_of_mass(skeleton.joints)

    # Calculate spine / torso height scale for scale invariance
    shoulder_left = skeleton.get_joint_by_name("left_shoulder")
    shoulder_right = skeleton.get_joint_by_name("right_shoulder")
    scale = 1.0

    if shoulder_left and shoulder_right:
        shoulder_mid_y = (shoulder_left.y + shoulder_right.y) / 2.0
        torso_height = abs(shoulder_mid_y - cy)
        if torso_height > 1e-4:
            scale = target_scale / (torso_height * 2.0)

    normalized_joints = []
    for j in skeleton.joints:
        norm_j = Joint(
            id=j.id,
            name=j.name,
            x=(j.x - cx) * scale,
            y=(j.y - cy) * scale,
            z=(j.z - cz) * scale,
            visibility=j.visibility,
            confidence=j.confidence,
        )
        normalized_joints.append(norm_j)

    return Skeleton(
        joints=normalized_joints,
        topology_name=skeleton.topology_name,
        person_id=skeleton.person_id,
        center_of_mass=(0.0, 0.0, 0.0),
    )


def skeleton_to_numpy(skeleton: Skeleton) -> np.ndarray:
    """Convert skeleton joints to NumPy array of shape (V, C) where C=(x, y, z, confidence).

    Args:
        skeleton: Skeleton instance.

    Returns:
        NumPy array of shape (N_joints, 4).
    """
    coords = [[j.x, j.y, j.z, j.confidence] for j in skeleton.joints]
    return np.array(coords, dtype=np.float32)
