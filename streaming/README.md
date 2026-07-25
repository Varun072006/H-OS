# Streaming

Real-time video and sensor stream processing for HumanOS.

## Modules

### `ingest/`
Stream ingestion from various sources:
- **RTSP**: IP camera streams
- **WebRTC**: Browser-based camera feeds
- **USB/V4L2**: Local USB cameras
- **File**: Pre-recorded video files (for development and testing)

### `pipeline/`
Stream processing pipeline:
- Frame decoding and color space conversion
- Resolution normalization
- Frame rate control
- Multi-stream synchronization
- Pipeline stage orchestration

### `buffer/`
Frame buffering and synchronization:
- Ring buffers for fixed-memory operation
- Multi-camera temporal synchronization
- Backpressure handling for slow consumers

## Design Principles

1. **Bounded Memory**: Streaming operates with fixed memory allocation (ring buffers), regardless of stream duration.
2. **Privacy-Aware**: Frames are available only within the streaming pipeline and are not persisted.
3. **Backpressure**: Slow downstream consumers do not cause unbounded memory growth.
