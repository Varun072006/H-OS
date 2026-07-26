"""Video file frame source implementation for offline video processing."""

import time
from pathlib import Path

from streaming.ingest.base import FramePacket, FrameSource

try:
    import cv2  # type: ignore
    OPENCV_AVAILABLE = True
except ImportError:
    OPENCV_AVAILABLE = False


class FileFrameSource(FrameSource):
    """FrameSource implementation for reading local MP4/AVI/MKV video files."""

    def __init__(self, file_path: str | Path) -> None:
        self.file_path = Path(file_path)
        self._cap = None
        self._frame_count = 0

    def open(self) -> None:
        """Open video file handle."""
        if not OPENCV_AVAILABLE:
            raise RuntimeError("OpenCV (cv2) is required for FileFrameSource")

        if not self.file_path.exists():
            raise FileNotFoundError(f"Video file not found at path: {self.file_path}")

        self._cap = cv2.VideoCapture(str(self.file_path))
        if not self._cap.isOpened():
            raise RuntimeError(f"Failed to open video file at {self.file_path}")
        self._frame_count = 0

    def read(self) -> FramePacket | None:
        """Read next frame from video file."""
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
            source_id=f"file:{self.file_path.name}",
        )

    def close(self) -> None:
        """Close video file handle."""
        if self._cap is not None:
            self._cap.release()
            self._cap = None

    @property
    def is_open(self) -> bool:
        """Check if file handle is active."""
        return self._cap is not None and self._cap.isOpened()
