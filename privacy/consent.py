"""Consent manager handling user opt-in and opt-out data collection preferences."""

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class UserConsent:
    """User privacy consent settings."""

    user_id: str
    allow_anonymous_motion_analysis: bool = True
    allow_telemetry: bool = False
    allow_model_training_opt_in: bool = False
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))


class ConsentManager:
    """Manager managing consent state storage and verification."""

    def __init__(self) -> None:
        self._consents: dict[str, UserConsent] = {}

    def set_consent(self, consent: UserConsent) -> None:
        """Store or update user consent settings."""
        self._consents[consent.user_id] = consent

    def get_consent(self, user_id: str) -> UserConsent:
        """Get consent settings for user, defaulting to privacy-safe default."""
        if user_id not in self._consents:
            return UserConsent(user_id=user_id)
        return self._consents[user_id]

    def is_action_allowed(self, user_id: str, action: str) -> bool:
        """Check if action is permitted under user consent."""
        consent = self.get_consent(user_id)
        if action == "motion_analysis":
            return consent.allow_anonymous_motion_analysis
        elif action == "telemetry":
            return consent.allow_telemetry
        elif action == "model_training":
            return consent.allow_model_training_opt_in
        return False
