"""Prediction module registry for plugin discovery and instantiation."""

from typing import Callable
from ai.predictions.base import PredictionModule

_PREDICTION_REGISTRY: dict[str, PredictionModule] = {}


def register_prediction_module(name: str) -> Callable[[type[PredictionModule]], type[PredictionModule]]:
    """Decorator registering a PredictionModule class under a string key name.

    Args:
        name: Unique module registration key (e.g. 'fall_risk', 'posture').
    """

    def decorator(cls: type[PredictionModule]) -> type[PredictionModule]:
        _PREDICTION_REGISTRY[name] = cls()  # Instantiate singleton instance
        return cls

    return decorator


def get_prediction_module(name: str) -> PredictionModule:
    """Retrieve registered PredictionModule instance by name.

    Args:
        name: Name of registered module.

    Returns:
        PredictionModule instance.
    """
    if name not in _PREDICTION_REGISTRY:
        raise ValueError(f"Unknown prediction module '{name}'. Available: {list(_PREDICTION_REGISTRY.keys())}")
    return _PREDICTION_REGISTRY[name]


def list_prediction_modules() -> list[str]:
    """List all registered prediction module names."""
    return list(_PREDICTION_REGISTRY.keys())
