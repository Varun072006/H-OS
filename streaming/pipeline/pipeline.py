"""StreamingPipeline main orchestrator executing continuous stream processing."""

from typing import Generator
from ai.pose.mediapipe_extractor import MediaPipePoseExtractor
from backend.schemas.responses import HumanStateResponse
from streaming.ingest.base import FrameSource
from streaming.pipeline.config import PipelineConfig
from streaming.pipeline.stages import PipelineStages


class StreamingPipeline:
    """End-to-end Streaming Processing Pipeline orchestrator."""

    def __init__(self, config: PipelineConfig | None = None) -> None:
        self.config = config or PipelineConfig()
        self.extractor = MediaPipePoseExtractor()
        self.extractor.initialize()

        self.stages = PipelineStages(
            extractor=self.extractor,
            topology_name=self.config.topology,
            window_size=self.config.window_size,
            device=self.config.device,
        )

    def run_stream(self, source: FrameSource, session_id: str = "live_stream") -> Generator[HumanStateResponse, None, None]:
        """Stream frames from source and yield real-time HumanStateResponse objects.

        Args:
            source: FrameSource handle (webcam, RTSP, video file).
            session_id: Session identifier string.

        Yields:
            HumanStateResponse update objects.
        """
        for packet in source.stream():
            state = self.stages.process_frame(
                frame=packet.frame,
                frame_index=packet.frame_index,
                session_id=session_id,
            )
            yield state

    def close(self) -> None:
        """Release underlying pipeline resources."""
        self.extractor.release()
