"""JWT Authentication token generation, decoding, and validation handler."""

import base64
import json
import time
import hmac
import hashlib


class JWTHandler:
    """JWT Token generator and verifier using HMAC-SHA256 (HS256)."""

    def __init__(self, secret_key: str = "humanos_jwt_secret_key_change_in_prod") -> None:
        self.secret_key = secret_key

    def _b64_encode(self, data: bytes) -> str:
        return base64.urlsafe_b64encode(data).rstrip(b"=").decode("utf-8")

    def _b64_decode(self, data: str) -> bytes:
        padding = "=" * (4 - (len(data) % 4))
        return base64.urlsafe_b64decode((data + padding).encode("utf-8"))

    def create_token(self, payload: dict, expires_in_seconds: int = 3600) -> str:
        """Create signed JWT access token.

        Args:
            payload: Dictionary claims payload.
            expires_in_seconds: Token validity duration.

        Returns:
            Signed JWT string 'header.payload.signature'.
        """
        header = {"alg": "HS256", "typ": "JWT"}
        now = int(time.time())

        claims = payload.copy()
        claims.update({"iat": now, "exp": now + expires_in_seconds})

        header_b64 = self._b64_encode(json.dumps(header).encode("utf-8"))
        payload_b64 = self._b64_encode(json.dumps(claims).encode("utf-8"))

        message = f"{header_b64}.{payload_b64}"
        signature = hmac.new(self.secret_key.encode("utf-8"), message.encode("utf-8"), hashlib.sha256).digest()
        sig_b64 = self._b64_encode(signature)

        return f"{message}.{sig_b64}"

    def decode_token(self, token: str) -> dict:
        """Decode and verify signature and expiration of JWT token.

        Args:
            token: JWT token string.

        Returns:
            Decoded payload claims dictionary if valid.
        """
        parts = token.split(".")
        if len(parts) != 3:
            raise ValueError("Invalid JWT token format")

        header_b64, payload_b64, sig_b64 = parts
        message = f"{header_b64}.{payload_b64}"

        expected_sig = hmac.new(self.secret_key.encode("utf-8"), message.encode("utf-8"), hashlib.sha256).digest()
        actual_sig = self._b64_decode(sig_b64)

        if not hmac.compare_digest(expected_sig, actual_sig):
            raise ValueError("Invalid token signature")

        claims = json.loads(self._b64_decode(payload_b64).decode("utf-8"))

        if "exp" in claims and claims["exp"] < int(time.time()):
            raise ValueError("JWT token has expired")

        return claims
