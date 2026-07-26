"""MotionGraphBuilder constructing spatiotemporal graphs from skeleton sequences."""

import numpy as np

from ai.graph.skeleton_config import get_topology
from ai.graph.types import MotionGraph
from ai.pose.types import Skeleton


class MotionGraphBuilder:
    """Builder class converting sequences of Skeleton objects into MotionGraph tensors."""

    def __init__(self, topology_name: str = "mediapipe_33") -> None:
        self.topology = get_topology(topology_name)
        self.spatial_edge_index = self._build_spatial_edge_index()

    def _build_spatial_edge_index(self) -> np.ndarray:
        """Construct 2xE spatial edge_index array from bone pairs."""
        edges = []
        # Add bidirectional bone pairs
        for u, v in self.topology.bone_pairs:
            edges.append((u, v))
            edges.append((v, u))

        # Add self loops
        for i in range(self.topology.num_joints):
            edges.append((i, i))

        return np.array(edges, dtype=np.int64).T  # Shape (2, E)

    def build_from_skeletons(
        self, skeletons: list[Skeleton], include_confidence: bool = True
    ) -> MotionGraph:
        """Build MotionGraph object from a temporal sequence of Skeleton instances.

        Args:
            skeletons: List of Skeleton objects [T frames].
            include_confidence: Whether to include joint confidence as 4th channel.

        Returns:
            MotionGraph dataclass containing feature tensor x (C, T, V) and edge_index.
        """
        num_frames = len(skeletons)
        num_joints = self.topology.num_joints
        num_channels = 4 if include_confidence else 3

        feature_tensor = np.zeros((num_channels, num_frames, num_joints), dtype=np.float32)

        for t, skel in enumerate(skeletons):
            for joint in skel.joints:
                if 0 <= joint.id < num_joints:
                    feature_tensor[0, t, joint.id] = joint.x
                    feature_tensor[1, t, joint.id] = joint.y
                    feature_tensor[2, t, joint.id] = joint.z
                    if include_confidence:
                        feature_tensor[3, t, joint.id] = joint.confidence

        return MotionGraph(
            x=feature_tensor,
            edge_index=self.spatial_edge_index,
            topology_name=self.topology.name,
            num_frames=num_frames,
            num_joints=num_joints,
        )

    def build_spatiotemporal_edge_index(self, num_frames: int) -> np.ndarray:
        """Construct combined 2x(E_spatial + E_temporal) edge index across temporal frames window T.

        Args:
            num_frames: Length T of temporal window.

        Returns:
            Combined edge index array of shape (2, E_total).
        """
        v_count = self.topology.num_joints
        edges = []

        # 1. Spatial edges for each temporal frame
        for t in range(num_frames):
            offset = t * v_count
            for u, v in self.topology.bone_pairs:
                edges.append((u + offset, v + offset))
                edges.append((v + offset, u + offset))

        # 2. Temporal edges connecting same joint across adjacent frames (t -> t+1)
        for t in range(num_frames - 1):
            offset_curr = t * v_count
            offset_next = (t + 1) * v_count
            for j in range(v_count):
                edges.append((j + offset_curr, j + offset_next))
                edges.append((j + offset_next, j + offset_curr))

        return np.array(edges, dtype=np.int64).T
