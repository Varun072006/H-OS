"""Analysis utilities for motion embeddings: cosine similarity, distance, drift detection."""

import numpy as np


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Compute cosine similarity between two motion embedding vectors.

    Args:
        a: Embedding array (D,).
        b: Embedding array (D,).

    Returns:
        Cosine similarity float [-1.0, 1.0].
    """
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a < 1e-6 or norm_b < 1e-6:
        return 0.0
    return float(np.dot(a, b) / (norm_a * norm_b))


def compute_embedding_drift(window: np.ndarray) -> float:
    """Compute mean step-to-step embedding variance/drift over a temporal window (T, D).

    Args:
        window: Array of shape (T, D).

    Returns:
        Average Euclidean distance between consecutive temporal embeddings.
    """
    if len(window) < 2:
        return 0.0

    diffs = np.linalg.norm(window[1:] - window[:-1], axis=1)
    return float(np.mean(diffs))
