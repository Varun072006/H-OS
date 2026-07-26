"""Session repository for CRUD database operations on camera sessions."""

from backend.database.models.session import DBSessionRecord


class SessionRepository:
    """Repository handling persistence operations for DBSessionRecord objects."""

    def __init__(self) -> None:
        self._records: dict[str, DBSessionRecord] = {}

    def save(self, record: DBSessionRecord) -> DBSessionRecord:
        """Save or update session record."""
        self._records[record.session_id] = record
        return record

    def get_by_id(self, session_id: str) -> DBSessionRecord | None:
        """Retrieve session record by session_id."""
        return self._records.get(session_id)

    def list_all(self) -> list[DBSessionRecord]:
        """List all session records."""
        return list(self._records.values())

    def delete(self, session_id: str) -> bool:
        """Delete session record."""
        if session_id in self._records:
            del self._records[session_id]
            return True
        return False
