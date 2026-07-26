"""Shared pytest configuration and fixtures for HumanOS tests."""

import pytest


@pytest.fixture
def sample_joint_coordinates() -> list[dict[str, float]]:
    """Sample normalized joint coordinates fixture for testing pose/graph utilities."""
    return [
        {"x": 0.5, "y": 0.2, "z": 0.0, "visibility": 0.99, "confidence": 0.95},
        {"x": 0.45, "y": 0.35, "z": 0.1, "visibility": 0.98, "confidence": 0.94},
        {"x": 0.55, "y": 0.35, "z": -0.1, "visibility": 0.97, "confidence": 0.92},
    ]
