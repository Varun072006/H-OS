"""WebSocket event message schemas."""

from pydantic import BaseModel, Field
from backend.schemas.responses import HumanStateResponse


class WSEvent(BaseModel):
    """Base WebSocket event payload container."""

    event_type: str = Field(..., description="Event type string ('state_update', 'alert', 'error')")
    data: dict = Field(default_factory=dict, description="Event payload dictionary")
