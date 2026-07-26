"""Database privacy audit log record model."""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class DBAuditRecord:
    """Privacy audit record representation for persistent storage."""

    entry_hash: str
    event_type: str
    details: dict[str, Any]
    previous_hash: str
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
