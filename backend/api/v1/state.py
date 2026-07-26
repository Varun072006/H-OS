"""Human state endpoints."""

import numpy as np
from fastapi import APIRouter, HTTPException, Depends
from backend.schemas.responses import HumanStateResponse
from backend.services.state_manager import HumanStateManager
from backend.services.session_manager import SessionManager
from backend.api.v1.sessions import get_session_manager

router = APIRouter(prefix="/sessions", tags=["Human State"])

_state_manager = HumanStateManager()


def get_state_manager() -> HumanStateManager:
    return _state_manager


@router.get("/{session_id}/state", response_model=HumanStateResponse)
async def get_human_state(
    session_id: str,
    sess_mgr: SessionManager = Depends(get_session_manager),
    state_mgr: HumanStateManager = Depends(get_state_manager),
) -> HumanStateResponse:
    """Get current continuous human physical state for a session."""
    session = sess_mgr.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found")

    # Generate current state update with synthetic/random motion embedding
    dummy_emb = np.random.randn(256).astype(np.float32)
    dummy_emb = dummy_emb / np.linalg.norm(dummy_emb)

    return state_mgr.update_state(session_id, dummy_emb)
