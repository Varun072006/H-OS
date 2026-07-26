"""Unit tests for Database layer models and repositories."""

from backend.database.models.session import DBSessionRecord
from backend.database.models.prediction import DBPredictionRecord
from backend.database.models.audit import DBAuditRecord
from backend.database.repositories.session_repo import SessionRepository
from backend.database.repositories.prediction_repo import PredictionRepository
from backend.database.repositories.audit_repo import AuditRepository


def test_session_repository() -> None:
    """Test SessionRepository CRUD methods."""
    repo = SessionRepository()
    record = DBSessionRecord(session_id="sess_100", camera_id="webcam:0")

    repo.save(record)
    assert repo.get_by_id("sess_100") == record
    assert len(repo.list_all()) == 1

    assert repo.delete("sess_100")
    assert repo.get_by_id("sess_100") is None


def test_prediction_repository() -> None:
    """Test PredictionRepository operations."""
    repo = PredictionRepository()
    record = DBPredictionRecord(
        id="pred_1",
        session_id="sess_100",
        module_name="fall_risk",
        label="Fall Risk Low",
        confidence=0.95,
        risk_level="low",
        score=0.1,
        contributing_features=[],
        model_version="v1.0",
    )

    repo.save(record)
    results = repo.get_by_session("sess_100")
    assert len(results) == 1
    assert results[0].label == "Fall Risk Low"


def test_audit_repository() -> None:
    """Test AuditRepository operations."""
    repo = AuditRepository()
    record = DBAuditRecord(
        entry_hash="hash_123",
        event_type="FRAME_DELETION",
        details={"status": "zeroed"},
        previous_hash="0" * 64,
    )

    repo.save(record)
    assert len(repo.list_all()) == 1
    assert repo.list_all()[0].entry_hash == "hash_123"
