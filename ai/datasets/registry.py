"""Dataset registry for config-driven dataset instantiation."""

from typing import Any, Callable

# Registry mapping dataset names to dataset class loader factories
_DATASET_REGISTRY: dict[str, Callable[..., Any]] = {}


def register_dataset(name: str) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Decorator registering a dataset class under a string key name.

    Args:
        name: Unique dataset registration key (e.g. 'ntu60', 'folder').
    """

    def decorator(cls: Callable[..., Any]) -> Callable[..., Any]:
        _DATASET_REGISTRY[name] = cls
        return cls

    return decorator


def get_dataset_class(name: str) -> Callable[..., Any]:
    """Retrieve dataset loader class by name.

    Args:
        name: Name of registered dataset.

    Returns:
        Dataset loader class factory.
    """
    if name not in _DATASET_REGISTRY:
        raise ValueError(f"Unknown dataset '{name}'. Available: {list(_DATASET_REGISTRY.keys())}")
    return _DATASET_REGISTRY[name]
