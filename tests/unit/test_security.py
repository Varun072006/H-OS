"""Unit tests for Security features: AES encryption, JWT authentication, RBAC, API keys."""

import pytest

from security.encryption.aes import AESCipher
from security.auth.jwt_handler import JWTHandler
from security.auth.rbac import RBACManager, Role
from security.policies.api_keys import APIKeyManager


def test_aes_encryption_decryption() -> None:
    """Test AES-256 cipher encryption and decryption round-trip."""
    cipher = AESCipher("secret_key_123")
    plain = "Confidential Human Motion Vector Data"

    ciphertext = cipher.encrypt(plain)
    assert ciphertext != plain

    decrypted = cipher.decrypt(ciphertext)
    assert decrypted == plain


def test_jwt_handler_create_and_decode() -> None:
    """Test JWT token generation and validation."""
    jwt_handler = JWTHandler("jwt_secret_key_456")
    payload = {"user_id": "usr_999", "role": "admin"}

    token = jwt_handler.create_token(payload, expires_in_seconds=60)
    assert isinstance(token, str)

    decoded = jwt_handler.decode_token(token)
    assert decoded["user_id"] == "usr_999"
    assert decoded["role"] == "admin"


def test_jwt_handler_invalid_signature() -> None:
    """Test JWT token forgery rejection."""
    jwt_handler1 = JWTHandler("secret_1")
    jwt_handler2 = JWTHandler("secret_2")

    token = jwt_handler1.create_token({"user_id": "usr_1"})
    with pytest.raises(ValueError, match="Invalid token signature"):
        jwt_handler2.decode_token(token)


def test_rbac_manager_permissions() -> None:
    """Test Role-Based Access Control authorization."""
    assert RBACManager.has_permission(Role.ADMIN, "model_manage")
    assert RBACManager.has_permission("admin", "privacy_audit")
    assert not RBACManager.has_permission(Role.VIEWER, "write")
    assert not RBACManager.has_permission("invalid_role", "read")


def test_api_key_manager() -> None:
    """Test API Key creation and validation."""
    mgr = APIKeyManager()
    raw_key, key_id = mgr.create_api_key("test_client", role="developer")

    assert raw_key.startswith("hos_")
    meta = mgr.validate_key(raw_key)
    assert meta is not None
    assert meta["client_name"] == "test_client"

    # Invalid key
    assert mgr.validate_key("hos_invalid") is None
