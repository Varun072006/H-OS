"""Unit tests for Motion Embeddings and all 5 Prediction Modules (FR-007, FR-008, FR-009)."""

import numpy as np
import pytest
import torch

from ai.embeddings.analysis import cosine_similarity, compute_embedding_drift
from ai.embeddings.extractor import MotionEmbeddingExtractor
from ai.embeddings.store import TemporalEmbeddingStore
from ai.models.stgcn.config import STGCNConfig
from ai.models.stgcn.model import STGCN
from ai.predictions.base import PredictionModule
from ai.predictions.registry import get_prediction_module, list_prediction_modules
from ai.predictions.types import Prediction, RiskLevel

# Import prediction modules to trigger auto-registration
import ai.predictions.fall_risk
import ai.predictions.posture
import ai.predictions.activity
import ai.predictions.rehabilitation
import ai.predictions.ergonomics


def test_motion_embedding_extractor() -> None:
    """Test MotionEmbeddingExtractor output shape and L2 normalization."""
    config = STGCNConfig(embedding_dim=256)
    model = STGCN(config)
    extractor = MotionEmbeddingExtractor(model)

    x = np.random.randn(4, 10, 33).astype(np.float32)
    emb = extractor.extract(x)

    assert isinstance(emb, np.ndarray)
    assert emb.shape == (256,)
    assert abs(float(np.linalg.norm(emb)) - 1.0) < 1e-4


def test_temporal_embedding_store() -> None:
    """Test sliding window temporal store buffer."""
    store = TemporalEmbeddingStore(max_window_size=5)
    for i in range(10):
        emb = np.full(128, i, dtype=np.float32)
        store.add(emb)

    window = store.get_window()
    assert window.shape == (5, 128)
    assert store.__len__() == 5
    assert window[0, 0] == 5  # Oldest in sliding window length 5
    assert window[4, 0] == 9  # Newest in sliding window


def test_embedding_analysis_functions() -> None:
    """Test cosine similarity and drift calculations."""
    a = np.array([1.0, 0.0, 0.0], dtype=np.float32)
    b = np.array([1.0, 0.0, 0.0], dtype=np.float32)
    c = np.array([0.0, 1.0, 0.0], dtype=np.float32)

    assert abs(cosine_similarity(a, b) - 1.0) < 1e-5
    assert abs(cosine_similarity(a, c) - 0.0) < 1e-5

    window = np.array([[0.0, 0.0], [1.0, 0.0], [2.0, 0.0]], dtype=np.float32)
    drift = compute_embedding_drift(window)
    assert abs(drift - 1.0) < 1e-5


def test_prediction_registry_and_all_modules() -> None:
    """Test registry listing and execution of all 5 prediction modules."""
    registered = list_prediction_modules()
    expected = ["fall_risk", "posture", "activity", "rehabilitation", "ergonomics"]
    for mod_name in expected:
        assert mod_name in registered

    emb = np.random.randn(256).astype(np.float32)
    emb = emb / np.linalg.norm(emb)
    context = np.random.randn(10, 256).astype(np.float32)

    for mod_name in expected:
        mod = get_prediction_module(mod_name)
        assert isinstance(mod, PredictionModule)
        pred = mod.predict(emb, context_window=context)

        assert isinstance(pred, Prediction)
        assert pred.module_name == mod_name
        assert 0.0 <= pred.confidence <= 1.0
        assert isinstance(pred.risk_level, RiskLevel)
        assert isinstance(pred.to_dict(), dict)
