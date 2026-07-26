"""Privacy audit log repository."""

from backend.database.models.audit import DBAuditRecord


class AuditRepository:
    """Repository handling persistence for privacy audit trail records."""

    def __init__(self) -> None:
        self._records: list[DBAuditRecord] = []

    def save(self, record: DBAuditRecord) -> DBAuditRecord:
        """Save privacy audit record."""
        self._records.append(record)
        return record

    def list_all(self) -> list[DBAuditRecord]:
        """List all audit records."""
        return list(self._records)
