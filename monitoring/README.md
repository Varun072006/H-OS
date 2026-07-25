# Monitoring

System health, performance observability, and alerting for HumanOS.

## Modules

### `telemetry/`
Metrics collection and export:
- **`metrics.py`** — Custom metric definitions (inference latency, throughput, queue depth, error rates)
- **`exporters/`** — Metric exporters for Prometheus, OpenTelemetry, and CloudWatch

### `dashboards/`
Pre-built monitoring dashboard configurations:
- Grafana dashboards for system health
- Inference performance dashboards
- Privacy audit dashboards

### `alerts/`
Alert rules and notification channels:
- Latency threshold alerts
- Error rate alerts
- Privacy violation alerts
- Resource utilization alerts

## Key Metrics

| Metric | Type | Description |
|--------|------|-------------|
| `humanos_inference_latency_ms` | Histogram | End-to-end inference latency |
| `humanos_frames_processed_total` | Counter | Total frames processed |
| `humanos_active_streams` | Gauge | Currently active camera streams |
| `humanos_privacy_frame_deletions_total` | Counter | Frames deleted after pose extraction |
| `humanos_prediction_confidence` | Histogram | Prediction confidence distribution |
