"""Skeleton topology configurations, joint indices, bone connections, and adjacency matrices."""

from dataclasses import dataclass
import numpy as np


@dataclass
class SkeletonTopology:
    """Topology definition for a human skeleton model."""

    name: str
    num_joints: int
    bone_pairs: list[tuple[int, int]]
    joint_names: list[str]

    def get_adjacency_matrix(self) -> np.ndarray:
        """Construct symmetric spatial adjacency matrix A (V x V) with self-loops."""
        a = np.eye(self.num_joints, dtype=np.float32)
        for i, j in self.bone_pairs:
            a[i, j] = 1.0
            a[j, i] = 1.0
        return a


# MediaPipe 33 Landmark Skeleton Topology
MEDIAPIPE_33_BONES: list[tuple[int, int]] = [
    # Face
    (0, 1), (1, 2), (2, 3), (3, 7),
    (0, 4), (4, 5), (5, 6), (6, 8),
    (9, 10),
    # Torso
    (11, 12), (11, 23), (12, 24), (23, 24),
    # Left Arm
    (11, 13), (13, 15), (15, 17), (15, 19), (15, 21), (17, 19),
    # Right Arm
    (12, 14), (14, 16), (16, 18), (16, 20), (16, 22), (18, 20),
    # Left Leg
    (23, 25), (25, 27), (27, 29), (27, 31), (29, 31),
    # Right Leg
    (24, 26), (26, 28), (28, 30), (28, 32), (30, 32),
]

# NTU RGB+D 25 Landmark Skeleton Topology
NTU_25_BONES: list[tuple[int, int]] = [
    (1, 2), (2, 21), (3, 21), (4, 3),        # Head & Spine
    (5, 21), (6, 5), (7, 6), (8, 7),         # Left Arm
    (9, 21), (10, 9), (11, 10), (12, 11),     # Right Arm
    (13, 1), (14, 13), (15, 14), (16, 15),   # Left Leg
    (17, 1), (18, 17), (19, 18), (20, 19),   # Right Leg
    (22, 8), (23, 8), (24, 12), (25, 12),    # Thumbs & Hands
]
# Convert 1-based indexing in NTU to 0-based
NTU_25_BONES_0INDEXED = [(u - 1, v - 1) for u, v in NTU_25_BONES]


TOPOLOGIES: dict[str, SkeletonTopology] = {
    "mediapipe_33": SkeletonTopology(
        name="mediapipe_33",
        num_joints=33,
        bone_pairs=MEDIAPIPE_33_BONES,
        joint_names=[f"joint_{i}" for i in range(33)],
    ),
    "ntu_25": SkeletonTopology(
        name="ntu_25",
        num_joints=25,
        bone_pairs=NTU_25_BONES_0INDEXED,
        joint_names=[f"joint_{i}" for i in range(25)],
    ),
}


def get_topology(name: str) -> SkeletonTopology:
    """Retrieve skeleton topology definition by name."""
    if name not in TOPOLOGIES:
        raise ValueError(f"Unknown topology name '{name}'. Available: {list(TOPOLOGIES.keys())}")
    return TOPOLOGIES[name]
