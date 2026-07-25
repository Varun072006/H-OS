# Benchmarks

Performance and accuracy benchmarks for HumanOS models and pipelines.

## Modules

### `accuracy/`
Model accuracy benchmarks:
- Action recognition accuracy on standard datasets (NTU RGB+D, Kinetics)
- Fall prediction recall and precision
- Motion forecasting error (MPJPE, FDE)

### `latency/`
Inference latency benchmarks:
- Per-stage latency profiling (pose extraction, graph construction, encoding, prediction)
- End-to-end pipeline latency
- Edge device latency (Jetson, Coral, RPi)

### `datasets/`
Benchmark dataset configurations and splits. Defines standard evaluation protocols for reproducibility.

## Running Benchmarks

```bash
# Run accuracy benchmarks
python -m benchmarks.accuracy.run --config configs/benchmark/ntu_xsub.yaml

# Run latency benchmarks
python -m benchmarks.latency.run --device gpu --warmup 100 --iterations 1000
```

## Results

Benchmark results are tracked in `docs/experiments/` and versioned with each release.
