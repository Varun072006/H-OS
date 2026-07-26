"""Causal inference chain container mapping observations -> inferences -> predictions -> intervention recommendations."""

from dataclasses import dataclass, field


@dataclass
class CausalChain:
    """Represents a multi-step causal reasoning chain.

    Observation -> Inference -> Prediction -> Recommendation
    """

    observation: str
    inference: str
    prediction: str
    recommendation: str
    confidence: float = 0.85
    metadata: dict = field(default_factory=dict)
