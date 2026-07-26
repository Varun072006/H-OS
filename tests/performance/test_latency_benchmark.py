"""Performance and inference latency benchmark test suite (SRS Target < 100ms)."""

import time
import pytest
import torch

from ai.models.stgcn.config import STGCNConfig
from ai.models.stgcn.model import STGCN


def test_stgcn_inference_latency_benchmark() -> None:
    """Benchmark STGCN forward pass latency (Target < 100ms per window)."""
    model = STGCN(STGCNConfig())
    model.eval()

    x = torch.randn(1, 4, 30, 33)

    # Warmup runs
    for _ in range(5):
        _ = model(x)

    # Benchmark 20 iterations
    start_time = time.perf_counter()
    iterations = 20
    for _ in range(iterations):
        _ = model(x)

    total_time_ms = (time.perf_counter() - start_time) * 1000.0
    avg_latency_ms = total_time_ms / iterations

    print(f"\nAverage Inference Latency: {avg_latency_ms:.2f} ms")
    assert avg_latency_ms < 100.0, f"Inference latency {avg_latency_ms:.2f}ms exceeded 100ms target"
