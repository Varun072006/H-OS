"""Data retention manager enforcing automatic data expiration and cleanup policies."""

from datetime import datetime, timedelta, timezone


class DataRetentionManager:
    """Manager enforcing data expiration limits."""

    def __init__(self, retention_days: int = 30) -> None:
        self.retention_days = retention_days

    def is_expired(self, created_at: datetime) -> bool:
        """Check if data record has exceeded retention period.

        Args:
            created_at: Datetime when record was created.

        Returns:
            True if record is past expiration cutoff date.
        """
        now = datetime.now(timezone.utc)
        if created_at.tzinfo is None:
            created_at = created_at.replace(tzinfo=timezone.utc)
        cutoff = now - timedelta(days=self.retention_days)
        return created_at < cutoff
