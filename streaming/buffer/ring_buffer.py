"""Bounded memory ring buffer for streaming video frames and features."""

from collections import deque
from typing import Generic, TypeVar

T = TypeVar("T")


class RingBuffer(Generic[T]):
    """Fixed-capacity memory ring buffer guaranteeing bounded memory usage during stream processing."""

    def __init__(self, capacity: int = 30) -> None:
        self.capacity = capacity
        self._queue: deque[T] = deque(maxlen=capacity)

    def push(self, item: T) -> None:
        """Push item into ring buffer, evicting oldest item if full."""
        self._queue.append(item)

    def get_all(self) -> list[T]:
        """Retrieve all items currently stored in buffer in chronological order."""
        return list(self._queue)

    def clear(self) -> None:
        """Empty all buffer items."""
        self._queue.clear()

    def is_full(self) -> bool:
        """Check if buffer has reached capacity."""
        return len(self._queue) == self.capacity

    def __len__(self) -> int:
        return len(self._queue)
