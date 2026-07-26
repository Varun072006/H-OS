"""Streaming pipeline configuration container."""

from dataclasses import dataclass, field


@dataclass
class PipelineConfig:
    """Configuration settings for streaming processing pipeline."""

    camera_id: str = "webcam:0"
    source_type: str = "webcam"
    target_fps: int = 30
    window_size: int = 30
    topology: str = "mediapipe_33"
    enable_privacy_zeroing: bool = True
    device: str = "cpu"
    prediction_modules: list[str] = field(default_factory=lambda: ["fall_risk", "posture", "activity"])
