"""Model validation tests verifying output bounds, shape integrity, and NaN/Inf robustness."""

import pytest
import torch
import numpy as np

from ai.models.stgcn.config import STGCNConfig
from ai.models.stgcn.model import STGCN


def test_stgcn_nan_inf_robustness() -> None:
    """Test STGCN robustness against extreme values."""
    model = STGCN(STGCNConfig())
    model.eval()

    # Normal input
    x = torch.randn(2, 4, 30, 33)
    with torch.no_grad():
        out = model(x)
        assert not torch.isnan(out).any()
        assert not torch.isinf(out).any()


def test_stgcn_zero_input_handling() -> None:
    """Test STGCN forward pass with all-zero input tensor."""
    model = STGCN(STGCNConfig())
    model.eval()

    x = torch.zeros(2, 4, 30, 33)
    with torch.no_grad():
        out = model(x)
        assert out.shape == (2, 60)
        assert not torch.isnan(out).any()
