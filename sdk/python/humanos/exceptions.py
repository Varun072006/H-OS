"""SDK exception hierarchy."""


class HumanOSError(Exception):
    """Base exception class for all HumanOS SDK errors."""

    pass


class APIError(HumanOSError):
    """Raised when the HumanOS API server returns an error response."""

    def __init__(self, status_code: int, message: str) -> None:
        self.status_code = status_code
        self.message = message
        super().__init__(f"APIError [{status_code}]: {message}")


class SessionError(HumanOSError):
    """Raised when session operations fail or session does not exist."""

    pass


class AuthenticationError(HumanOSError):
    """Raised when authentication or API key validation fails."""

    pass
