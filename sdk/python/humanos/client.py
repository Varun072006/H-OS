"""HumanOS main Python client SDK class."""

import httpx
from sdk.python.humanos.exceptions import APIError
from sdk.python.humanos.models import SDKHumanState, SDKPrediction, SessionInfo
from sdk.python.humanos.session import Session


class HumanOSClient:
    """Python Client SDK for communicating with HumanOS platform APIs."""

    def __init__(
        self,
        endpoint: str = "http://localhost:8000",
        api_key: str | None = None,
        timeout: float = 10.0,
    ) -> None:
        self.endpoint = endpoint.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
        self.headers = {"Content-Type": "application/json"}
        if api_key:
            self.headers["X-API-Key"] = api_key

    def _get_client(self) -> httpx.Client:
        return httpx.Client(base_url=self.endpoint, headers=self.headers, timeout=self.timeout)

    def health(self) -> dict:
        """Check API server health."""
        with self._get_client() as client:
            resp = client.get("/v1/health")
            if resp.status_code != 200:
                raise APIError(resp.status_code, resp.text)
            return resp.json()

    def create_session(
        self, camera_id: str, source_type: str = "webcam", topology: str = "mediapipe_33"
    ) -> Session:
        """Create a new camera stream session."""
        payload = {
            "camera_id": camera_id,
            "source_type": source_type,
            "topology": topology,
        }
        with self._get_client() as client:
            resp = client.post("/v1/sessions", json=payload)
            if resp.status_code != 200:
                raise APIError(resp.status_code, resp.text)
            data = resp.json()
            info = SessionInfo(**data)
            return Session(self, info)

    def list_sessions(self) -> list[SessionInfo]:
        """List active sessions."""
        with self._get_client() as client:
            resp = client.get("/v1/sessions")
            if resp.status_code != 200:
                raise APIError(resp.status_code, resp.text)
            return [SessionInfo(**s) for s in resp.json()]

    def get_human_state(self, session_id: str) -> SDKHumanState:
        """Get continuous human state for session."""
        with self._get_client() as client:
            resp = client.get(f"/v1/sessions/{session_id}/state")
            if resp.status_code != 200:
                raise APIError(resp.status_code, resp.text)
            data = resp.json()
            preds = [SDKPrediction(**p) for p in data["predictions"]]
            return SDKHumanState(
                session_id=data["session_id"],
                timestamp=data["timestamp"],
                has_pose=data["has_pose"],
                posture_quality=data["posture_quality"],
                gait_stability=data["gait_stability"],
                fatigue_score=data["fatigue_score"],
                predictions=preds,
            )

    def close_session(self, session_id: str) -> bool:
        """Close camera session."""
        with self._get_client() as client:
            resp = client.delete(f"/v1/sessions/{session_id}")
            return resp.status_code == 200
