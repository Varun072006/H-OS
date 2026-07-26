"""Abstract Base Class interface for video/sensor frame ingestion sources."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generator

import numpy as np


@dataclass
class FramePacket:
    """Container for a single ingested frame and metadata.

    Attributes:
        frame: Image pixel array (H, W, C).
        frame_index: Sequential frame number.
        timestamp: Unix timestamp in seconds.
        source_id: Unique identifier for sensor/camera.
    """

    frame: np.ndarray
    frame_index: int
    timestamp: float
    source_id: str


class FrameSource(ABC):
    """Abstract interface defining contracts for frame ingest sources (Webcam, RTSP, Video File)."""

    @abstractmethod
    def open(self) -> None:
        """Open camera device or media file stream."""
        ...

    @abstractmethod
    def read(self) -> FramePacket | None:
        """Fetch next frame packet from stream.

        Returns:
            FramePacket or None if stream ended or frame unavailable.
        """
        ...

    @abstractmethod
    def close(self) -> None:
        """Release underlying camera or stream handle."""
        ...

    @property
    @abstractmethod
    def is_open(self) -> bool:
        """Check if source stream is active and open."""
        ...

    def stream(self) -> Generator[FramePacket, None, None]:
        """Yield frame packets sequentially as a generator."""
        if not self.is_open:
            self.open()
        try:
            while self.is_open:
                packet = self.read()
                if packet is None:
                    break
                yield packet
        finally:
            self.close()

    def __enter__(self) -> "FrameSource":
        self.open()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()
