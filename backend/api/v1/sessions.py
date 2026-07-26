"""Session management endpoints."""

from fastapi import APIRouter, HTTPException, Depends
from backend.schemas.requests import SessionCreateRequest
from backend.schemas.responses import SessionResponse
from backend.services.session_manager import SessionManager

router = APIRouter(prefix="/sessions", tags=["Sessions"])

_session_manager = SessionManager()


def get_session_manager() -> SessionManager:
    return _session_manager


@router.post("", response_model=SessionResponse)
async def create_session(
    req: SessionCreateRequest,
    mgr: SessionManager = Depends(get_session_manager),
) -> SessionResponse:
    """Create a new camera stream processing session."""
    session = mgr.create_session(
        camera_id=req.camera_id,
        source_type=req.source_type,
        topology=req.topology,
    )
    return SessionResponse(**session)


@router.get("", response_model=list[SessionResponse])
async def list_sessions(
    mgr: SessionManager = Depends(get_session_manager),
) -> list[SessionResponse]:
    """List all active sessions."""
    sessions = mgr.list_sessions()
    return [SessionResponse(**s) for s in sessions]


@router.get("/{session_id}", response_model=SessionResponse)
async def get_session(
    session_id: str,
    mgr: SessionManager = Depends(get_session_manager),
) -> SessionResponse:
    """Get session by ID."""
    session = mgr.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found")
    return SessionResponse(**session)


@router.delete("/{session_id}")
async def close_session(
    session_id: str,
    mgr: SessionManager = Depends(get_session_manager),
) -> dict:
    """Close and terminate a session."""
    success = mgr.close_session(session_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found")
    return {"status": "closed", "session_id": session_id}
