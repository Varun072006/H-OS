"""Guaranteed raw video frame deletion and zero-fill memory clearing context manager."""

import hashlib
import time
from typing import Any
import numpy as np

from ai.pose.base import PoseExtractor
from ai.pose.types import PoseResult
from privacy.audit_log import PrivacyAuditLogger


class PrivacyBoundary:
    """Context manager enforcing the hard privacy boundary:

    1. Accepts raw camera video frame in memory.
    2. Invokes PoseExtractor to extract skeletal joint landmarks.
    3. Guarantees raw frame numpy buffer is overwritten with zeros (zero-filled).
    4. Logs immutable cryptographic audit record of frame deletion.
    """

    def __init__(self, audit_logger: PrivacyAuditLogger | None = None) -> None:
        self.audit_logger = audit_logger or PrivacyAuditLogger()

    def extract_and_delete(
        self, frame: np.ndarray, extractor: PoseExtractor, frame_index: int = 0
    ) -> PoseResult:
        """Extract skeletal landmarks and immediately overwrite raw video frame pixels with zeros.

        Args:
            frame: Input video pixel array (H, W, C).
            extractor: PoseExtractor backend handle.
            frame_index: Sequential frame number.

        Returns:
            PoseResult containing anonymous skeletal landmarks only.
        """
        # 1. Compute frame SHA-256 hash for audit proof before deletion
        frame_bytes = frame.tobytes()
        frame_hash = hashlib.sha256(frame_bytes).hexdigest()

        try:
            # 2. Extract pose landmarks
            pose_result = extractor.extract(frame, frame_index=frame_index)
        finally:
            # 3. GUARANTEED ZERO-FILL: Overwrite raw pixel array memory with zeros
            frame.fill(0)

            # 4. Record cryptographic deletion proof in audit log
            self.audit_logger.log_frame_deletion(
                frame_hash=frame_hash,
                frame_index=frame_index,
                landmarks_extracted=pose_result.has_pose,
            )

        return pose_result

    def __enter__(self) -> "PrivacyBoundary":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        pass
