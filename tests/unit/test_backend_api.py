"""Unit/Integration tests for FastAPI backend server endpoints."""

import pytest
from fastapi.testclient import TestClient

from backend.main import app

client = TestClient(app)


def test_health_check_endpoint() -> None:
    """Test GET /v1/health endpoint."""
    response = client.get("/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["version"] == "0.1.0"


def test_session_lifecycle_endpoints() -> None:
    """Test POST, GET, and DELETE /v1/sessions endpoints."""
    # 1. Create session
    payload = {
        "camera_id": "webcam:0",
        "source_type": "webcam",
        "topology": "mediapipe_33",
    }
    res_create = client.post("/v1/sessions", json=payload)
    assert res_create.status_code == 200
    sess_data = res_create.json()
    assert "session_id" in sess_data
    session_id = sess_data["session_id"]

    # 2. Get session
    res_get = client.get(f"/v1/sessions/{session_id}")
    assert res_get.status_code == 200
    assert res_get.json()["session_id"] == session_id

    # 3. List sessions
    res_list = client.get("/v1/sessions")
    assert res_list.status_code == 200
    assert len(res_list.json()) >= 1

    # 4. Get human state
    res_state = client.get(f"/v1/sessions/{session_id}/state")
    assert res_state.status_code == 200
    state_data = res_state.json()
    assert state_data["session_id"] == session_id
    assert len(state_data["predictions"]) > 0

    # 5. Delete session
    res_del = client.delete(f"/v1/sessions/{session_id}")
    assert res_del.status_code == 200


def test_prediction_endpoints() -> None:
    """Test GET /v1/predictions/modules and POST /v1/predictions/analyze."""
    res_mods = client.get("/v1/predictions/modules")
    assert res_mods.status_code == 200
    mods = res_mods.json()
    assert "fall_risk" in mods

    payload = {"prediction_module": "fall_risk", "joints": []}
    res_analyze = client.post("/v1/predictions/analyze", json=payload)
    assert res_analyze.status_code == 200
    data = res_analyze.json()
    assert data["module_name"] == "fall_risk"


def test_models_and_batch_endpoints() -> None:
    """Test GET /v1/models and POST /v1/batch/analyze endpoints."""
    res_models = client.get("/v1/models")
    assert res_models.status_code == 200
    assert len(res_models.json()) >= 1

    batch_payload = {"file_path": "data/sample.mp4", "prediction_modules": ["fall_risk"]}
    res_batch = client.post("/v1/batch/analyze", json=batch_payload)
    assert res_batch.status_code == 200
    assert "job_id" in res_batch.json()
