"""WebSocket streaming handler for real-time human state & predictions (FR-014)."""

import asyncio
import json
import numpy as np
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from backend.services.state_manager import HumanStateManager

router = APIRouter(tags=["Streaming WebSocket"])

_state_manager = HumanStateManager()


@router.websocket("/ws/stream/{session_id}")
async def websocket_stream_endpoint(websocket: WebSocket, session_id: str) -> None:
    """WebSocket stream endpoint pushing real-time human state updates."""
    await websocket.accept()
    try:
        while True:
            # Generate continuous synthetic embedding for real-time test streaming
            emb = np.random.randn(256).astype(np.float32)
            emb = emb / np.linalg.norm(emb)

            state = _state_manager.update_state(session_id, emb)
            payload = {
                "event_type": "state_update",
                "data": state.model_dump(),
            }
            await websocket.send_text(json.dumps(payload))

            # Stream at ~10 Hz update frequency
            await asyncio.sleep(0.1)
    except WebSocketDisconnect:
        pass
