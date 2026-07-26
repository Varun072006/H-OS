"""Camera session lifecycle manager."""

import uuid
from datetime import datetime, timezone


class SessionManager:
    """Manager handling active camera sessions, status tracking, and metadata."""

    def __init__(self) -> None:
        self._sessions: dict[str, dict] = {}

    def create_session(self, camera_id: str, source_type: str = "webcam", topology: str = "mediapipe_33") -> dict:
        """Create and index a new active camera processing session.

        Returns:
            Session dictionary containing session_id and metadata.
        """
        session_id = f"sess_{uuid.uuid4().hex[:12]}"
        created_at = datetime.now(timezone.utc).isoformat()

        session = {
            "session_id": session_id,
            "camera_id": camera_id,
            "source_type": source_type,
            "topology": topology,
            "status": "active",
            "created_at": created_at,
        }
        self._sessions[session_id] = session
        return session

    def get_session(self, session_id: str) -> dict | None:
        """Retrieve session by ID."""
        return self._sessions.get(session_id)

    def list_sessions(self) -> list[dict]:
        """List all active sessions."""
        return list(self._sessions.values())

    def close_session(self, session_id: str) -> bool:
        """Close and remove session."""
        if session_id in self._sessions:
            self._sessions[session_id]["status"] = "closed"
            return True
        return False
