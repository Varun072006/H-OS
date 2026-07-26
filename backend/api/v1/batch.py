"""Batch offline motion analysis endpoints (FR-015)."""

import uuid
from fastapi import APIRouter
from backend.schemas.requests import BatchAnalyzeRequest

router = APIRouter(prefix="/batch", tags=["Batch Processing"])


@router.post("/analyze")
async def submit_batch_job(req: BatchAnalyzeRequest) -> dict:
    """Submit video file or skeleton array for offline batch motion analysis."""
    job_id = f"batch_{uuid.uuid4().hex[:12]}"
    return {
        "job_id": job_id,
        "file_path": req.file_path,
        "status": "queued",
        "modules": req.prediction_modules,
        "message": "Batch motion analysis job submitted successfully",
    }
