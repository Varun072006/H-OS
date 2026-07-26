"""Unit tests for HumanOS Python Client SDK."""

import pytest
from sdk.python.humanos.client import HumanOSClient
from sdk.python.humanos.exceptions import APIError
from sdk.python.humanos.models import SDKHumanState, SessionInfo


def test_sdk_client_initialization() -> None:
    """Test SDK Client creation and endpoint normalization."""
    client = HumanOSClient(endpoint="http://localhost:8000/")
    assert client.endpoint == "http://localhost:8000"


def test_sdk_mock_client_calls(monkeypatch) -> None:
    """Test SDK method calls against mocked httpx responses."""
    client = HumanOSClient(endpoint="http://localhost:8000")

    # Test health check structure
    dummy_health = {"status": "ok", "version": "0.1.0"}

    class DummyResponse:
        status_code = 200

        def json(self):
            return dummy_health

    class DummyHTTPClient:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

        def get(self, url):
            return DummyResponse()

    monkeypatch.setattr(client, "_get_client", lambda: DummyHTTPClient())

    res = client.health()
    assert res["status"] == "ok"
