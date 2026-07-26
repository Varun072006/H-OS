"""Data types and data structures for human pose representation."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class Joint:
    """Represents a single anatomical landmark/joint in 2D or 3D space.

    Attributes:
        id: Joint index or landmark ID (e.g. MediaPipe 0..32).
        name: Human-readable joint name (e.g. 'left_shoulder').
        x: Normalized X coordinate [0.0, 1.0] or meters.
        y: Normalized Y coordinate [0.0, 1.0] or meters.
        z: Depth coordinate or estimated depth in meters.
        visibility: Likelihood of landmark being visible/unoccluded [0.0, 1.0].
        confidence: Landmark extraction confidence score [0.0, 1.0].
    """

    id: int
    name: str
    x: float
    y: float
    z: float = 0.0
    visibility: float = 1.0
    confidence: float = 1.0

    def to_dict(self) -> dict[str, Any]:
        """Serialize joint to dictionary representation."""
        return {
            "id": self.id,
            "name": self.name,
            "x": round(self.x, 5),
            "y": round(self.y, 5),
            "z": round(self.z, 5),
            "visibility": round(self.visibility, 4),
            "confidence": round(self.confidence, 4),
        }


@dataclass
class Skeleton:
    """Represents a full human skeleton pose at a single instant.

    Attributes:
        joints: List of Joint objects forming the body skeleton.
        topology_name: Name of joint topology scheme (e.g. 'mediapipe_33', 'ntu_25').
        person_id: Identifier for person in multi-person tracking contexts.
        center_of_mass: Calculated (x, y, z) midpoint of hips/torso.
    """

    joints: list[Joint]
    topology_name: str = "mediapipe_33"
    person_id: int = 0
    center_of_mass: tuple[float, float, float] = field(default=(0.0, 0.0, 0.0))

    def get_joint_by_name(self, name: str) -> Joint | None:
        """Find joint by its landmark name."""
        for joint in self.joints:
            if joint.name == name:
                return joint
        return None

    def get_joint_by_id(self, joint_id: int) -> Joint | None:
        """Find joint by numerical ID."""
        for joint in self.joints:
            if joint.id == joint_id:
                return joint
        return None

    def to_dict(self) -> dict[str, Any]:
        """Serialize skeleton to dictionary representation."""
        return {
            "topology_name": self.topology_name,
            "person_id": self.person_id,
            "center_of_mass": self.center_of_mass,
            "joints": [j.to_dict() for j in self.joints],
        }


@dataclass
class PoseResult:
    """Output container returned by a PoseExtractor for a single frame.

    Attributes:
        skeletons: List of detected Skeleton instances (1 for single-person, multiple for multi-person).
        timestamp: Timestamp of frame capture/processing in UTC.
        frame_index: Sequential index of frame in stream/video.
        detection_confidence: Overall pose detector confidence.
        processing_time_ms: Extraction latency in milliseconds.
    """

    skeletons: list[Skeleton]
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    frame_index: int = 0
    detection_confidence: float = 1.0
    processing_time_ms: float = 0.0

    @property
    def has_pose(self) -> bool:
        """Check if any valid human skeleton was detected in the frame."""
        return len(self.skeletons) > 0 and len(self.skeletons[0].joints) > 0
