"""API Key management and validation policies."""

import hashlib
import secrets


class APIKeyManager:
    """Manager issuing and validating API key credentials."""

    def __init__(self) -> None:
        self._keys: dict[str, dict] = {}  # Hashed key -> metadata

    def create_api_key(self, client_name: str, role: str = "developer") -> tuple[str, str]:
        """Generate a new secure API key.

        Returns:
            Tuple of (raw_api_key, key_id).
        """
        raw_key = f"hos_{secrets.token_urlsafe(32)}"
        key_hash = hashlib.sha256(raw_key.encode("utf-8")).hexdigest()
        key_id = secrets.token_hex(8)

        self._keys[key_hash] = {
            "key_id": key_id,
            "client_name": client_name,
            "role": role,
            "active": True,
        }
        return raw_key, key_id

    def validate_key(self, raw_api_key: str) -> dict | None:
        """Validate raw API key.

        Returns:
            Key metadata dict if active and valid, None otherwise.
        """
        key_hash = hashlib.sha256(raw_api_key.encode("utf-8")).hexdigest()
        meta = self._keys.get(key_hash)
        if meta and meta.get("active"):
            return meta
        return None
