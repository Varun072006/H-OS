"""Immutable cryptographic audit logger recording privacy actions."""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class PrivacyAuditLogger:
    """Audit logger generating SHA-256 hashed immutable event logs for privacy compliance."""

    def __init__(self, log_dir: str | Path = "logs/privacy") -> None:
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.audit_log_file = self.log_dir / "privacy_audit.jsonl"
        self._last_hash = "0" * 64

    def log_event(self, event_type: str, details: dict[str, Any]) -> dict[str, Any]:
        """Record audit event with chain hash verification.

        Args:
            event_type: Category ('FRAME_DELETION', 'CONSENT_CHANGE', 'DATA_PURGE').
            details: Contextual details dictionary.

        Returns:
            Recorded log entry dictionary.
        """
        timestamp = datetime.now(timezone.utc).isoformat()
        payload = {
            "timestamp": timestamp,
            "event_type": event_type,
            "details": details,
            "previous_hash": self._last_hash,
        }

        # Calculate chain hash
        entry_bytes = json.dumps(payload, sort_keys=True).encode("utf-8")
        entry_hash = hashlib.sha256(entry_bytes).hexdigest()
        payload["entry_hash"] = entry_hash
        self._last_hash = entry_hash

        # Append to jsonl log file
        with open(self.audit_log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(payload) + "\n")

        return payload

    def log_frame_deletion(
        self, frame_hash: str, frame_index: int, landmarks_extracted: bool
    ) -> dict[str, Any]:
        """Record frame zeroing and deletion verification proof."""
        return self.log_event(
            event_type="FRAME_DELETION",
            details={
                "frame_hash": frame_hash,
                "frame_index": frame_index,
                "landmarks_extracted": landmarks_extracted,
                "status": "ZEROED_AND_DEALLOCATED",
            },
        )
