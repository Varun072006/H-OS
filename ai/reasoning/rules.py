"""Rule-based risk reasoning chains."""

from dataclasses import dataclass


@dataclass
class ReasoningRule:
    """Rule definition for risk reasoning."""

    rule_id: str
    condition_feature: str
    threshold: float
    comparison: str  # 'gt', 'lt'
    recommendation: str


DEFAULT_RULES: list[ReasoningRule] = [
    ReasoningRule(
        rule_id="RULE_FALL_HIGH",
        condition_feature="gait_instability",
        threshold=0.5,
        comparison="gt",
        recommendation="Suggest seated rest and alert caregiver or safety supervisor.",
    ),
    ReasoningRule(
        rule_id="RULE_POSTURE_UNSAFE",
        condition_feature="spinal_flexion_angle",
        threshold=0.4,
        comparison="gt",
        recommendation="Adjust lifting technique; keep back straight and bend knees.",
    ),
]
