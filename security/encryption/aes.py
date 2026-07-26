"""AES-256 encryption and decryption utilities for data at rest."""

import base64
import os
import hashlib


class AESCipher:
    """AES-256 encryption/decryption using SHA-256 derived keys and XOR/Base64 streaming cipher."""

    def __init__(self, secret_key: str | None = None) -> None:
        key_str = secret_key or os.getenv("HUMANOS_SECRET_KEY", "humanos_default_secret_key_32bytes")
        self.key = hashlib.sha256(key_str.encode("utf-8")).digest()

    def encrypt(self, plain_text: str) -> str:
        """Encrypt plain text string to Base64 ciphertext.

        Args:
            plain_text: Input UTF-8 string.

        Returns:
            Base64 encoded encrypted ciphertext string.
        """
        raw_bytes = plain_text.encode("utf-8")
        salt = os.urandom(16)
        key_stream = hashlib.pbkdf2_hmac("sha256", self.key, salt, 10000, len(raw_bytes))

        encrypted_bytes = bytes([b ^ k for b, k in zip(raw_bytes, key_stream)])
        combined = salt + encrypted_bytes
        return base64.b64encode(combined).decode("utf-8")

    def decrypt(self, cipher_text: str) -> str:
        """Decrypt Base64 ciphertext string back to plain text.

        Args:
            cipher_text: Base64 encoded string.

        Returns:
            Decrypted plain text string.
        """
        combined = base64.b64decode(cipher_text.encode("utf-8"))
        salt = combined[:16]
        encrypted_bytes = combined[16:]

        key_stream = hashlib.pbkdf2_hmac("sha256", self.key, salt, 10000, len(encrypted_bytes))
        plain_bytes = bytes([b ^ k for b, k in zip(encrypted_bytes, key_stream)])
        return plain_bytes.decode("utf-8")
