"""Database session record model."""

from dataclasses import dataclass, field
from datetime import datetime, timezone


@dataclass
class DBSessionRecord:
    """Session record representation for persistent storage."""

    session_id: str
    camera_id: str
    source_type: str = "webcam"
    topology: str = "mediapipe_33"
    status: str = "active"
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    closed_at: datetime | None = None
