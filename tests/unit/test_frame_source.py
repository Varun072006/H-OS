"""Unit tests for streaming frame sources (webcam, file, base interface)."""

import numpy as np
import pytest

from streaming.ingest.base import FramePacket, FrameSource


class MockFrameSource(FrameSource):
    """Mock frame source for unit testing streaming interface contracts."""

    def __init__(self, total_frames: int = 5) -> None:
        self.total_frames = total_frames
        self._current_frame = 0
        self._is_open = False

    def open(self) -> None:
        self._is_open = True
        self._current_frame = 0

    def read(self) -> FramePacket | None:
        if not self._is_open or self._current_frame >= self.total_frames:
            return None

        self._current_frame += 1
        dummy_frame = np.zeros((100, 100, 3), dtype=np.uint8)
        return FramePacket(
            frame=dummy_frame,
            frame_index=self._current_frame,
            timestamp=1000.0 + self._current_frame,
            source_id="mock_camera",
        )

    def close(self) -> None:
        self._is_open = False

    @property
    def is_open(self) -> bool:
        return self._is_open


def test_frame_packet_creation() -> None:
    """Test FramePacket container fields."""
    dummy_frame = np.zeros((480, 640, 3), dtype=np.uint8)
    packet = FramePacket(
        frame=dummy_frame,
        frame_index=1,
        timestamp=123456.78,
        source_id="webcam:0",
    )
    assert packet.frame_index == 1
    assert packet.source_id == "webcam:0"
    assert packet.frame.shape == (480, 640, 3)


def test_mock_frame_source_context_manager() -> None:
    """Test FrameSource context manager and stream generator."""
    with MockFrameSource(total_frames=3) as source:
        assert source.is_open
        packets = list(source.stream())
        assert len(packets) == 3
        assert packets[0].frame_index == 1
        assert packets[2].frame_index == 3

    assert not source.is_open
