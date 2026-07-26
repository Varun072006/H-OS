"""Stress and concurrency test simulating load."""

import concurrent.futures
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


def _make_request(session_id: str) -> int:
    response = client.get(f"/v1/sessions/{session_id}/state")
    return response.status_code


def test_concurrent_api_stress() -> None:
    """Stress test API with concurrent simulated user requests."""
    # First create session
    create_res = client.post("/v1/sessions", json={"camera_id": "stress_cam"})
    session_id = create_res.json()["session_id"]

    # Execute 20 concurrent requests
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(_make_request, session_id) for _ in range(20)]
        results = [f.result() for f in concurrent.futures.as_completed(futures)]

    assert all(code == 200 for code in results)
