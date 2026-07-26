"""Minimal Skeleton Tracking Demo."""

from streaming.ingest.base import FrameSource
from streaming.pipeline.config import PipelineConfig
from streaming.pipeline.pipeline import StreamingPipeline
from tests.integration.test_streaming_pipeline import MockFrameStreamSource


def main() -> None:
    print("=== HumanOS Minimal Tracking Demo ===")
    config = PipelineConfig(window_size=5)
    pipeline = StreamingPipeline(config)
    source = MockFrameStreamSource(count=3)

    for state in pipeline.run_stream(source, session_id="demo_session"):
        print(f"[{state.timestamp}] Session: {state.session_id} | Predictions: {len(state.predictions)}")

    pipeline.close()


if __name__ == "__main__":
    main()
