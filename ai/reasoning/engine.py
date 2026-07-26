"""Main ReasoningEngine evaluating rules and generating causal intervention recommendations."""

from ai.predictions.types import Prediction
from ai.reasoning.causal import CausalChain
from ai.reasoning.rules import DEFAULT_RULES, ReasoningRule


class ReasoningEngine:
    """Reasoning engine producing causal chains and intervention recommendations for predictions."""

    def __init__(self, rules: list[ReasoningRule] | None = None) -> None:
        self.rules = rules or DEFAULT_RULES

    def evaluate_prediction(self, prediction: Prediction) -> CausalChain | None:
        """Evaluate prediction and generate causal chain with actionable recommendation.

        Args:
            prediction: Input Prediction object.

        Returns:
            CausalChain object if rule matched, or None.
        """
        for feat in prediction.contributing_features:
            feat_name = feat.get("feature", "")
            importance = feat.get("importance", 0.0)

            for rule in self.rules:
                if rule.condition_feature == feat_name:
                    matched = (
                        (importance > rule.threshold)
                        if rule.comparison == "gt"
                        else (importance < rule.threshold)
                    )
                    if matched:
                        return CausalChain(
                            observation=f"Feature '{feat_name}' measured at {importance:.2f}",
                            inference=f"Sustained pattern exceeds threshold {rule.threshold}",
                            prediction=prediction.label,
                            recommendation=rule.recommendation,
                            confidence=prediction.confidence,
                        )
        return None
