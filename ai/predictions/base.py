"""Abstract Base Class interface for pluggable prediction modules."""

from abc import ABC, abstractmethod
import numpy as np

from ai.predictions.types import Prediction


class PredictionModule(ABC):
    """Abstract interface contract for all domain-specific prediction modules."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Module identifier string name."""
        ...

    @abstractmethod
    def predict(
        self, embedding: np.ndarray, context_window: np.ndarray | None = None
    ) -> Prediction:
        """Generate prediction given a motion embedding vector.

        Args:
            embedding: Motion embedding vector of shape (D,) or (1, D).
            context_window: Optional sliding window tensor of past embeddings (T, D).

        Returns:
            Prediction object containing label, confidence, risk_level, and metadata.
        """
        ...
