"""Unit tests for Telemetry metrics and Prometheus exporter."""

from monitoring.telemetry.exporters.prometheus import export_prometheus_metrics
from monitoring.telemetry.metrics import (
    ACTIVE_STREAMS,
    FRAME_DELETIONS_TOTAL,
    FRAMES_PROCESSED_TOTAL,
    INFERENCE_LATENCY_MS,
)


def test_metrics_collection_and_prometheus_export() -> None:
    """Test metric increment, observation, and Prometheus text formatting."""
    FRAMES_PROCESSED_TOTAL.inc(10)
    FRAME_DELETIONS_TOTAL.inc(10)
    ACTIVE_STREAMS.set(2)
    INFERENCE_LATENCY_MS.observe(15.5)

    prom_text = export_prometheus_metrics()
    assert "humanos_frames_processed_total" in prom_text
    assert "humanos_privacy_frame_deletions_total" in prom_text
    assert "humanos_active_streams" in prom_text
    assert "humanos_inference_latency_ms" in prom_text
