"""Privacy compliance tests verifying frame zeroing, audit logs, anonymization, consent."""

from pathlib import Path
import numpy as np
import pytest

from ai.pose.mediapipe_extractor import MediaPipePoseExtractor
from ai.pose.types import Joint, Skeleton
from privacy.anonymization import anonymize_skeleton
from privacy.audit_log import PrivacyAuditLogger
from privacy.consent import ConsentManager, UserConsent
from privacy.frame_deletion import PrivacyBoundary
from privacy.retention import DataRetentionManager


def test_privacy_boundary_frame_zero_filling(tmp_path: Path) -> None:
    """CRITICAL PRIVACY TEST: Verify raw video frame buffer is zero-filled after extraction."""
    audit_logger = PrivacyAuditLogger(log_dir=tmp_path)
    boundary = PrivacyBoundary(audit_logger=audit_logger)
    extractor = MediaPipePoseExtractor()

    # Create dummy non-zero video frame array
    frame = np.ones((100, 100, 3), dtype=np.uint8) * 255
    assert np.max(frame) == 255

    # Run pose extraction through privacy boundary
    result = boundary.extract_and_delete(frame, extractor=extractor, frame_index=1)

    # 1. VERIFY FRAME IS ZERO-FILLED: Max value in array must be 0
    assert np.max(frame) == 0
    assert np.all(frame == 0)

    # 2. VERIFY AUDIT LOG RECORD CREATED
    audit_file = tmp_path / "privacy_audit.jsonl"
    assert audit_file.exists()
    content = audit_file.read_text(encoding="utf-8")
    assert "FRAME_DELETION" in content
    assert "ZEROED_AND_DEALLOCATED" in content


def test_skeleton_anonymization() -> None:
    """Test stripping facial features and personal identity landmarks."""
    joints = [
        Joint(id=0, name="nose", x=0.5, y=0.2, z=0.0),
        Joint(id=11, name="left_shoulder", x=0.4, y=0.35, z=0.0),
    ]
    skel = Skeleton(joints=joints)
    anon_skel = anonymize_skeleton(skel)

    # Facial landmark (id=0) coordinates zeroed
    assert anon_skel.joints[0].x == 0.0
    assert anon_skel.joints[0].y == 0.0

    # Body landmark (id=11) coordinates preserved
    assert anon_skel.joints[1].x == 0.4


def test_consent_manager() -> None:
    """Test consent settings opt-in/opt-out preferences."""
    mgr = ConsentManager()
    user_id = "user_123"

    assert mgr.is_action_allowed(user_id, "motion_analysis")
    assert not mgr.is_action_allowed(user_id, "telemetry")

    mgr.set_consent(UserConsent(user_id=user_id, allow_telemetry=True))
    assert mgr.is_action_allowed(user_id, "telemetry")


def test_data_retention_manager() -> None:
    """Test retention expiration policy check."""
    mgr = DataRetentionManager(retention_days=7)
    from datetime import datetime, timedelta, timezone

    old_date = datetime.now(timezone.utc) - timedelta(days=10)
    recent_date = datetime.now(timezone.utc) - timedelta(days=1)

    assert mgr.is_expired(old_date)
    assert not mgr.is_expired(recent_date)
