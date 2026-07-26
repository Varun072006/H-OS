"""MediaPipe Pose Estimation Backend Implementation."""

import time
from datetime import datetime, timezone
import numpy as np

from ai.pose.base import PoseExtractor
from ai.pose.types import Joint, PoseResult, Skeleton
from ai.pose.utils import MEDIAPIPE_JOINT_NAMES, calculate_center_of_mass

try:
    import mediapipe as mp  # type: ignore
    MEDIAPIPE_AVAILABLE = True
except ImportError:
    MEDIAPIPE_AVAILABLE = False


class MediaPipePoseExtractor(PoseExtractor):
    """PoseExtractor implementation utilizing Google MediaPipe Pose framework.

    Extracts 33 anatomical 3D body landmarks in real-time.
    """

    def __init__(
        self,
        static_image_mode: bool = False,
        model_complexity: int = 1,
        smooth_landmarks: bool = True,
        min_detection_confidence: float = 0.5,
        min_tracking_confidence: float = 0.5,
    ) -> None:
        self.static_image_mode = static_image_mode
        self.model_complexity = model_complexity
        self.smooth_landmarks = smooth_landmarks
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence
        self._pose_solution = None

    def initialize(self) -> None:
        """Instantiate MediaPipe Pose pipeline."""
        if MEDIAPIPE_AVAILABLE:
            mp_pose = mp.solutions.pose
            self._pose_solution = mp_pose.Pose(
                static_image_mode=self.static_image_mode,
                model_complexity=self.model_complexity,
                smooth_landmarks=self.smooth_landmarks,
                min_detection_confidence=self.min_detection_confidence,
                min_tracking_confidence=self.min_tracking_confidence,
            )

    def extract(self, frame: np.ndarray, frame_index: int = 0) -> PoseResult:
        """Process an RGB frame and extract MediaPipe landmarks.

        Args:
            frame: Image array (H, W, 3) in RGB or BGR format.
            frame_index: Sequential frame number.

        Returns:
            PoseResult object containing single or no skeleton.
        """
        start_time = time.perf_counter()

        if self._pose_solution is None and MEDIAPIPE_AVAILABLE:
            self.initialize()

        joints: list[Joint] = []
        if self._pose_solution is not None and MEDIAPIPE_AVAILABLE:
            # MediaPipe expects RGB
            if frame.ndim == 3 and frame.shape[2] == 3:
                results = self._pose_solution.process(frame)
                if results and results.pose_landmarks:
                    for idx, lm in enumerate(results.pose_landmarks.landmark):
                        name = (
                            MEDIAPIPE_JOINT_NAMES[idx]
                            if idx < len(MEDIAPIPE_JOINT_NAMES)
                            else f"joint_{idx}"
                        )
                        joint = Joint(
                            id=idx,
                            name=name,
                            x=float(lm.x),
                            y=float(lm.y),
                            z=float(lm.z),
                            visibility=float(getattr(lm, "visibility", 1.0)),
                            confidence=float(getattr(lm, "presence", 1.0)),
                        )
                        joints.append(joint)

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        skeletons = []
        if joints:
            center = calculate_center_of_mass(joints)
            skeleton = Skeleton(
                joints=joints,
                topology_name="mediapipe_33",
                person_id=0,
                center_of_mass=center,
            )
            skeletons.append(skeleton)

        return PoseResult(
            skeletons=skeletons,
            timestamp=datetime.now(timezone.utc),
            frame_index=frame_index,
            detection_confidence=1.0 if joints else 0.0,
            processing_time_ms=elapsed_ms,
        )

    def release(self) -> None:
        """Close MediaPipe solution resources."""
        if self._pose_solution is not None:
            self._pose_solution.close()
            self._pose_solution = None
