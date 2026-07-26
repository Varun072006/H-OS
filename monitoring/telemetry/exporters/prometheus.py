"""Prometheus metrics exporter formatting in-memory metrics for scraping."""

from monitoring.telemetry.metrics import (
    ACTIVE_STREAMS,
    API_REQUEST_LATENCY_MS,
    FRAME_DELETIONS_TOTAL,
    FRAMES_PROCESSED_TOTAL,
    INFERENCE_LATENCY_MS,
)


def export_prometheus_metrics() -> str:
    """Format in-memory metrics into Prometheus text format string.

    Returns:
        Prometheus plain text formatted metrics string.
    """
    lines = [
        f"# HELP {FRAMES_PROCESSED_TOTAL.name} Total frames processed by HumanOS",
        f"# TYPE {FRAMES_PROCESSED_TOTAL.name} counter",
        f"{FRAMES_PROCESSED_TOTAL.name} {FRAMES_PROCESSED_TOTAL.value}",
        "",
        f"# HELP {FRAME_DELETIONS_TOTAL.name} Total frames zero-filled & deleted",
        f"# TYPE {FRAME_DELETIONS_TOTAL.name} counter",
        f"{FRAME_DELETIONS_TOTAL.name} {FRAME_DELETIONS_TOTAL.value}",
        "",
        f"# HELP {ACTIVE_STREAMS.name} Active camera processing streams",
        f"# TYPE {ACTIVE_STREAMS.name} gauge",
        f"{ACTIVE_STREAMS.name} {ACTIVE_STREAMS.value}",
        "",
        f"# HELP {INFERENCE_LATENCY_MS.name} Mean ST-GCN inference latency in ms",
        f"# TYPE {INFERENCE_LATENCY_MS.name} gauge",
        f"{INFERENCE_LATENCY_MS.name} {INFERENCE_LATENCY_MS.mean:.2f}",
        "",
        f"# HELP {API_REQUEST_LATENCY_MS.name} Mean API request latency in ms",
        f"# TYPE {API_REQUEST_LATENCY_MS.name} gauge",
        f"{API_REQUEST_LATENCY_MS.name} {API_REQUEST_LATENCY_MS.mean:.2f}",
    ]
    return "\n".join(lines) + "\n"
