"""Integration tests for end-to-end streaming pipeline processing."""

import numpy as np
import pytest
from backend.schemas.responses import HumanStateResponse
from streaming.buffer.ring_buffer import RingBuffer
from streaming.buffer.sync import synchronize_multi_stream
from streaming.ingest.base import FramePacket, FrameSource
from streaming.pipeline.config import PipelineConfig
from streaming.pipeline.pipeline import StreamingPipeline


class MockFrameStreamSource(FrameSource):
    """Mock frame stream yielding 5 frames for testing pipeline."""

    def __init__(self, count: int = 5) -> None:
        self.count = count
        self.curr = 0
        self._is_open = False

    def open(self) -> None:
        self._is_open = True
        self.curr = 0

    def read(self) -> FramePacket | None:
        if not self._is_open or self.curr >= self.count:
            return None
        self.curr += 1
        frame = np.ones((100, 100, 3), dtype=np.uint8) * 128
        return FramePacket(frame=frame, frame_index=self.curr, timestamp=float(self.curr), source_id="mock_stream")

    def close(self) -> None:
        self._is_open = False

    @property
    def is_open(self) -> bool:
        return self._is_open


def test_ring_buffer_bounded_capacity() -> None:
    """Test RingBuffer capacity constraint."""
    buf: RingBuffer[int] = RingBuffer(capacity=3)
    for i in range(10):
        buf.push(i)

    assert len(buf) == 3
    assert buf.get_all() == [7, 8, 9]


def test_multi_stream_sync() -> None:
    """Test multi-camera temporal frame synchronizer."""
    data = {
        "cam1": [{"timestamp": 1.0, "id": "f1"}, {"timestamp": 2.0, "id": "f2"}],
        "cam2": [{"timestamp": 1.02, "id": "f1_sync"}, {"timestamp": 2.01, "id": "f2_sync"}],
    }
    synced = synchronize_multi_stream(data, time_tolerance_sec=0.05)
    assert len(synced) == 2
    assert synced[0]["cam1"]["id"] == "f1"
    assert synced[0]["cam2"]["id"] == "f1_sync"


def test_streaming_pipeline_end_to_end() -> None:
    """Test end-to-end streaming pipeline processing from mock frame source."""
    config = PipelineConfig(window_size=5, device="cpu")
    pipeline = StreamingPipeline(config)

    source = MockFrameStreamSource(count=3)
    results = list(pipeline.run_stream(source, session_id="test_stream_sess"))

    assert len(results) == 3
    for res in results:
        assert isinstance(res, HumanStateResponse)
        assert res.session_id == "test_stream_sess"
        assert len(res.predictions) > 0

    pipeline.close()
