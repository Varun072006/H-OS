"""In-memory sliding window buffer for storing temporal sequence of motion embeddings."""

from collections import deque
import numpy as np


class TemporalEmbeddingStore:
    """Sliding window buffer for accumulating motion embeddings over time steps T."""

    def __init__(self, max_window_size: int = 30) -> None:
        self.max_window_size = max_window_size
        self._buffer: deque[np.ndarray] = deque(maxlen=max_window_size)

    def add(self, embedding: np.ndarray) -> None:
        """Add single motion embedding vector (D,) to sliding window buffer."""
        self._buffer.append(embedding.flatten())

    def get_window(self) -> np.ndarray:
        """Get accumulated window array of shape (T_curr, D).

        Returns:
            NumPy array of shape (T, D) or empty array if empty.
        """
        if not self._buffer:
            return np.empty((0, 0), dtype=np.float32)
        return np.array(list(self._buffer), dtype=np.float32)

    def clear(self) -> None:
        """Clear all stored embeddings."""
        self._buffer.clear()

    def __len__(self) -> int:
        return len(self._buffer)
