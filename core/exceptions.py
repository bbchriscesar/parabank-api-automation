"""
Custom exception classes for the API automation framework.
Provides granular error types for better debugging and test reporting.
"""


class APIError(Exception):
    """Base exception for all API-related errors."""

    def __init__(self, message: str, status_code: int | None = None, response_body: str | None = None):
        self.status_code = status_code
        self.response_body = response_body
        super().__init__(message)


class APITimeoutError(APIError):
    """Raised when an API request exceeds the configured timeout."""
    pass


class APIConnectionError(APIError):
    """Raised when the API client cannot establish a connection."""
    pass
