"""Session handle for executing queries on a camera stream."""

from typing import TYPE_CHECKING
from sdk.python.humanos.models import SDKHumanState, SessionInfo

if TYPE_CHECKING:
    from sdk.python.humanos.client import HumanOSClient


class Session:
    """Active session instance bound to a camera stream."""

    def __init__(self, client: "HumanOSClient", info: SessionInfo) -> None:
        self.client = client
        self.info = info
        self.session_id = info.session_id

    def get_state(self) -> SDKHumanState:
        """Fetch current continuous human state for session."""
        return self.client.get_human_state(self.session_id)

    def close(self) -> bool:
        """Close this session."""
        return self.client.close_session(self.session_id)
