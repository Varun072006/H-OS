"""Data structure definitions for motion graph representations."""

from dataclasses import dataclass
import numpy as np


@dataclass
class MotionGraph:
    """Spatiotemporal Graph tensor data container for a skeleton motion sequence.

    Attributes:
        x: Node feature tensor of shape (C, T, V) or (N, C, T, V).
           C = Channels (e.g. 3 for x,y,z or 4 for x,y,z,confidence).
           T = Temporal frames window length.
           V = Number of vertices/joints.
        edge_index: Spatial-temporal edge indices tensor of shape (2, E).
        topology_name: Name of skeleton joint topology ('mediapipe_33', 'ntu_25').
        num_frames: Length T of temporal window.
        num_joints: Number V of joint nodes.
    """

    x: np.ndarray
    edge_index: np.ndarray
    topology_name: str
    num_frames: int
    num_joints: int

    def __post_init__(self) -> None:
        """Validate array dimensions."""
        if self.x.ndim not in (3, 4):
            raise ValueError(f"Feature tensor x must be 3D (C, T, V) or 4D (N, C, T, V), got shape {self.x.shape}")
