"""Pydantic request schemas for FastAPI endpoints."""

from pydantic import BaseModel, Field


class SessionCreateRequest(BaseModel):
    """Request payload for starting a new camera session."""

    camera_id: str = Field(..., description="Unique camera identifier or device path (e.g. 'webcam:0')")
    source_type: str = Field("webcam", description="Source type: 'webcam', 'rtsp', 'file'")
    window_size: int = Field(30, description="Sliding window size in frames")
    topology: str = Field("mediapipe_33", description="Joint topology scheme")


class BatchAnalyzeRequest(BaseModel):
    """Request payload for submitting batch offline motion analysis (FR-015)."""

    file_path: str = Field(..., description="Path to video file or skeleton npy array file")
    prediction_modules: list[str] = Field(
        default_factory=lambda: ["fall_risk", "posture", "activity"],
        description="List of prediction module names to execute",
    )


class DirectAnalyzeRequest(BaseModel):
    """Request payload for analyzing a direct array of joint landmarks."""

    joints: list[dict] = Field(..., description="List of joint landmark dicts")
    prediction_module: str = Field("fall_risk", description="Target prediction module name")
