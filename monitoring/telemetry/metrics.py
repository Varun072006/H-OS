"""Custom telemetry metrics definitions for HumanOS."""

import time
from dataclasses import dataclass, field


@dataclass
class Counter:
    """Simple in-memory metric counter."""

    name: str
    value: float = 0.0

    def inc(self, amount: float = 1.0) -> None:
        self.value += amount


@dataclass
class Gauge:
    """Simple in-memory metric gauge."""

    name: str
    value: float = 0.0

    def set(self, val: float) -> None:
        self.value = val


@dataclass
class Histogram:
    """Simple in-memory metric histogram measuring latency distributions."""

    name: str
    observations: list[float] = field(default_factory=list)

    def observe(self, val: float) -> None:
        self.observations.append(val)
        if len(self.observations) > 1000:
            self.observations.pop(0)

    @property
    def mean(self) -> float:
        return sum(self.observations) / max(1, len(self.observations))


# Telemetry metrics registry
INFERENCE_LATENCY_MS = Histogram("humanos_inference_latency_ms")
FRAMES_PROCESSED_TOTAL = Counter("humanos_frames_processed_total")
ACTIVE_STREAMS = Gauge("humanos_active_streams")
FRAME_DELETIONS_TOTAL = Counter("humanos_privacy_frame_deletions_total")
API_REQUEST_LATENCY_MS = Histogram("humanos_api_request_latency_ms")
