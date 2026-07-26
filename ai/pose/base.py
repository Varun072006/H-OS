"""Abstract Base Class interface for Pose Extraction backends."""

from abc import ABC, abstractmethod
from typing import Any

import numpy as np

from ai.pose.types import PoseResult


class PoseExtractor(ABC):
    """Abstract interface defining contracts for all pose estimation backends (MediaPipe, ViTPose, OpenPose)."""

    @abstractmethod
    def initialize(self) -> None:
        """Initialize models, weights, or hardware acceleration handles."""
        ...

    @abstractmethod
    def extract(self, frame: np.ndarray, frame_index: int = 0) -> PoseResult:
        """Extract human skeletal landmarks from a single RGB/BGR image frame.

        Args:
            frame: Input video frame as a NumPy array (H, W, 3).
            frame_index: Sequential integer index of the frame.

        Returns:
            PoseResult containing detected skeletons and metadata.
        """
        ...

    @abstractmethod
    def release(self) -> None:
        """Release underlying GPU/CPU memory and resources."""
        ...

    def __enter__(self) -> "PoseExtractor":
        self.initialize()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.release()
