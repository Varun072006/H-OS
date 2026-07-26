"""Unit tests for pose extraction data structures, utilities, and MediaPipe backend."""

import json
from pathlib import Path
import numpy as np

from ai.pose.types import Joint, Skeleton, PoseResult
from ai.pose.utils import (
    calculate_center_of_mass,
    normalize_skeleton,
    skeleton_to_numpy,
)
from ai.pose.mediapipe_extractor import MediaPipePoseExtractor


def test_joint_dataclass_and_serialization() -> None:
    """Test Joint object creation and to_dict method."""
    joint = Joint(id=0, name="nose", x=0.5, y=0.2, z=0.1, visibility=0.9, confidence=0.95)
    d = joint.to_dict()

    assert d["id"] == 0
    assert d["name"] == "nose"
    assert d["x"] == 0.5
    assert d["y"] == 0.2
    assert d["z"] == 0.1
    assert d["confidence"] == 0.95


def test_skeleton_center_of_mass_calculation() -> None:
    """Test center of mass calculation from hips."""
    joints = [
        Joint(id=23, name="left_hip", x=0.4, y=0.6, z=0.0),
        Joint(id=24, name="right_hip", x=0.6, y=0.6, z=0.0),
    ]
    cm = calculate_center_of_mass(joints)
    assert cm == (0.5, 0.6, 0.0)


def test_normalize_skeleton() -> None:
    """Test normalization to body-centered origin."""
    joints = [
        Joint(id=11, name="left_shoulder", x=0.4, y=0.3, z=0.0),
        Joint(id=12, name="right_shoulder", x=0.6, y=0.3, z=0.0),
        Joint(id=23, name="left_hip", x=0.4, y=0.6, z=0.0),
        Joint(id=24, name="right_hip", x=0.6, y=0.6, z=0.0),
    ]
    skeleton = Skeleton(joints=joints)
    norm_skel = normalize_skeleton(skeleton)

    # Hip center should be shifted to (0, 0, 0)
    norm_cm = calculate_center_of_mass(norm_skel.joints)
    assert abs(norm_cm[0]) < 1e-4
    assert abs(norm_cm[1]) < 1e-4


def test_skeleton_to_numpy_conversion() -> None:
    """Test conversion of skeleton joints to NumPy array."""
    joints = [
        Joint(id=0, name="nose", x=0.5, y=0.2, z=0.1, confidence=0.95),
        Joint(id=1, name="left_eye", x=0.45, y=0.18, z=0.1, confidence=0.94),
    ]
    skeleton = Skeleton(joints=joints)
    arr = skeleton_to_numpy(skeleton)

    assert isinstance(arr, np.ndarray)
    assert arr.shape == (2, 4)
    assert arr[0, 0] == 0.5
    assert arr[0, 3] == 0.95


def test_fixture_loading() -> None:
    """Test loading sample skeleton fixture JSON."""
    fixture_path = Path(__file__).parent / "fixtures" / "sample_skeleton.json"
    with open(fixture_path, encoding="utf-8") as f:
        data = json.load(f)

    joints = [Joint(**j) for j in data["joints"]]
    skeleton = Skeleton(joints=joints, topology_name=data["topology_name"])

    assert len(skeleton.joints) == 5
    assert skeleton.get_joint_by_name("nose") is not None


def test_mediapipe_pose_extractor_fallback() -> None:
    """Test MediaPipe extractor initialization and blank image processing."""
    extractor = MediaPipePoseExtractor()
    extractor.initialize()

    blank_frame = np.zeros((480, 640, 3), dtype=np.uint8)
    result = extractor.extract(blank_frame, frame_index=1)

    assert isinstance(result, PoseResult)
    assert result.frame_index == 1
    assert result.processing_time_ms >= 0.0
    extractor.release()
