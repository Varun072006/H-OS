"""Unit tests for Spatial Temporal Graph Convolutional Network (ST-GCN) model."""

import pytest
import torch

from ai.models.stgcn.config import STGCNConfig
from ai.models.stgcn.model import STGCN


def test_stgcn_initialization_and_forward_shape() -> None:
    """Test STGCN initialization and output tensor shapes."""
    config = STGCNConfig(
        in_channels=4,
        num_classes=10,
        graph_layout="mediapipe_33",
        num_joints=33,
        embedding_dim=128,
    )
    model = STGCN(config)
    model.eval()

    # Input tensor shape: (batch_size=2, C=4, T=30, V=33)
    x = torch.randn(2, 4, 30, 33)

    with torch.no_grad():
        logits = model(x)
        assert logits.shape == (2, 10)

        embedding = model.extract_embedding(x)
        assert embedding.shape == (2, 128)

        logits_ret, emb_ret = model(x, return_embedding=True)
        assert logits_ret.shape == (2, 10)
        assert emb_ret.shape == (2, 128)


def test_stgcn_gradient_flow() -> None:
    """Test backward pass and gradient flow through all STGCN layers."""
    config = STGCNConfig(
        in_channels=4,
        num_classes=5,
        graph_layout="mediapipe_33",
        num_joints=33,
    )
    model = STGCN(config)
    model.train()

    x = torch.randn(2, 4, 16, 33, requires_grad=True)
    target = torch.tensor([0, 2], dtype=torch.long)

    logits = model(x)
    loss = torch.nn.functional.cross_entropy(logits, target)
    loss.backward()

    # Verify input gradient is computed
    assert x.grad is not None
    assert torch.abs(x.grad).sum().item() > 0.0

    # Verify weight gradients are computed across layers
    for name, param in model.named_parameters():
        if param.requires_grad:
            assert param.grad is not None, f"Parameter {name} has no gradient"


def test_stgcn_embedding_normalization() -> None:
    """Test that output motion embeddings are L2 normalized (unit length)."""
    config = STGCNConfig(embedding_dim=256)
    model = STGCN(config)
    model.eval()

    x = torch.randn(4, 4, 20, 33)
    with torch.no_grad():
        emb = model.extract_embedding(x)
        norms = torch.norm(emb, p=2, dim=1)
        # L2 norm of each embedding vector should be ~1.0
        assert torch.allclose(norms, torch.ones_like(norms), atol=1e-4)
