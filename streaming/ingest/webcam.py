"""Webcam / USB camera frame source implementation using OpenCV."""

import time
import numpy as np

from streaming.ingest.base import FramePacket, FrameSource

try:
    import cv2  # type: ignore
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False


class WebcamFrameSource(FrameSource):
    """FrameSource implementation for USB / integrated webcams using OpenCV VideoCapture."""

    def __init__(
        self,
        camera_id: int | str = 0,
        fps: int = 30,
        width: int = 640,
        height: int = 480,
    ) -> None:
        self.camera_id = camera_id
        self.fps = fps
        self.width = width
        self.height = height
        self._cap = None
        self._frame_count = 0

    def open(self) -> None:
        """Open OpenCV VideoCapture handle."""
        if not OPENCV_AVAILABLE:
            raise RuntimeError("OpenCV (cv2) is required for WebcamFrameSource")

        self._cap = cv2.VideoCapture(self.camera_id)
        if not self._cap.isOpened():
            raise RuntimeError(f"Failed to open webcam source with camera_id={self.camera_id}")

        self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.width)
        self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.height)
        self._cap.set(cv2.CAP_PROP_FPS, self.fps)
        self._frame_count = 0

    def read(self) -> FramePacket | None:
        """Read single frame from webcam handle."""
        if self._cap is None or not self._cap.isOpened():
            return None

        ret, frame = self._cap.read()
        if not ret or frame is None:
            return None

        self._frame_count += 1
        return FramePacket(
            frame=frame,
            frame_index=self._frame_count,
            timestamp=time.time(),
            source_id=f"webcam:{self.camera_id}",
        )

    def close(self) -> None:
        """Release VideoCapture handle."""
        if self._cap is not None:
            self._cap.release()
            self._cap = None

    @property
    def is_open(self) -> bool:
        """Check if camera handle is active."""
        return self._cap is not None and self._cap.isOpened()
