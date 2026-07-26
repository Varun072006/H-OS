"""Unit tests for MotionGraphBuilder, normalization, topology, and augmentations."""

import numpy as np
import pytest

from ai.graph.builder import MotionGraphBuilder
from ai.graph.skeleton_config import get_topology
from ai.graph.normalization import normalize_motion_tensor
from ai.graph.augmentation import (
    random_joint_jitter,
    random_spatial_rotation,
    temporal_crop_or_pad,
)
from ai.pose.types import Joint, Skeleton


def test_get_topology_valid_and_invalid() -> None:
    """Test retrieving topology definition and error handling."""
    topo = get_topology("mediapipe_33")
    assert topo.num_joints == 33
    adj = topo.get_adjacency_matrix()
    assert adj.shape == (33, 33)

    with pytest.raises(ValueError, match="Unknown topology name"):
        get_topology("nonexistent_topology")


def test_motion_graph_builder_from_skeletons() -> None:
    """Test building MotionGraph from a sequence of skeletons."""
    builder = MotionGraphBuilder("mediapipe_33")

    # Create dummy 10-frame skeleton sequence
    skeletons = []
    for t in range(10):
        joints = [
            Joint(id=i, name=f"j_{i}", x=0.1 * i, y=0.2 * i, z=0.0, confidence=0.9)
            for i in range(33)
        ]
        skeletons.append(Skeleton(joints=joints))

    graph = builder.build_from_skeletons(skeletons, include_confidence=True)

    assert graph.x.shape == (4, 10, 33)  # C=4, T=10, V=33
    assert graph.num_frames == 10
    assert graph.num_joints == 33
    assert graph.edge_index.shape[0] == 2


def test_build_spatiotemporal_edge_index() -> None:
    """Test constructing spatiotemporal edges across T frames."""
    builder = MotionGraphBuilder("ntu_25")
    edges = builder.build_spatiotemporal_edge_index(num_frames=5)

    assert edges.ndim == 2
    assert edges.shape[0] == 2
    assert edges.shape[1] > 0


def test_normalize_motion_tensor() -> None:
    """Test motion tensor normalization function."""
    # Create tensor (C=4, T=10, V=33)
    x = np.ones((4, 10, 33), dtype=np.float32)
    x[0, :, :] += 5.0  # Shift coordinates

    norm_x = normalize_motion_tensor(x, center_joint_idx=0)
    assert norm_x.shape == (4, 10, 33)
    # Center joint (idx 0) x,y,z should be 0 across all time steps
    assert float(np.max(np.abs(norm_x[:3, :, 0]))) < 1e-5


def test_graph_augmentations() -> None:
    """Test graph level augmentations (jitter, rotation, temporal pad/crop)."""
    x = np.ones((4, 10, 33), dtype=np.float32)

    jittered = random_joint_jitter(x, std=0.05, p=1.0)
    assert jittered.shape == x.shape
    assert not np.array_equal(jittered[:3], x[:3])

    rotated = random_spatial_rotation(x, max_degrees=10.0, p=1.0)
    assert rotated.shape == x.shape

    padded = temporal_crop_or_pad(x, target_frames=20)
    assert padded.shape == (4, 20, 33)

    cropped = temporal_crop_or_pad(x, target_frames=5)
    assert cropped.shape == (4, 5, 33)


def np_allabs(arr: np.ndarray) -> float:
    return float(np.max(np.abs(arr)))
