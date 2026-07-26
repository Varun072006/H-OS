"""Prediction repository for logging prediction results."""

from backend.database.models.prediction import DBPredictionRecord


class PredictionRepository:
    """Repository handling persistence operations for DBPredictionRecord objects."""

    def __init__(self) -> None:
        self._records: list[DBPredictionRecord] = []

    def save(self, record: DBPredictionRecord) -> DBPredictionRecord:
        """Save prediction record."""
        self._records.append(record)
        return record

    def get_by_session(self, session_id: str) -> list[DBPredictionRecord]:
        """Fetch all prediction records for a specific session."""
        return [r for r in self._records if r.session_id == session_id]

    def list_recent(self, limit: int = 50) -> list[DBPredictionRecord]:
        """List most recent prediction records."""
        return self._records[-limit:]
