"""CSRF protection for Refast.

Provides Cross-Site Request Forgery protection using double-submit cookie pattern
with HMAC-SHA256 signed tokens.

Example:
    Using CSRFProtection:

    ```python
    from refast.security import CSRFProtection, CSRFConfig

    # Create with default config
    csrf = CSRFProtection(secret_key="your-secret-key")

    # Or with custom config
    config = CSRFConfig(
        token_expiry=7200,  # 2 hours
        cookie_name="csrf_token",
        header_name="X-CSRF-Token",
    )
    csrf = CSRFProtection(secret_key="your-secret-key", config=config)

    # Generate token
    token = csrf.generate_token()

    # Validate token
    if csrf.validate_token(token):
        print("Token is valid")

    # Use decorator for endpoints
    @app.post("/submit")
    @csrf_protect(csrf)
    async def submit(request: Request):
        # Protected endpoint
        pass
    ```
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import secrets
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from functools import wraps
from typing import TYPE_CHECKING, Any

from fastapi import HTTPException, Request
from starlette.responses import Response

if TYPE_CHECKING:
    pass


@dataclass
class CSRFConfig:
    """
    Configuration for CSRF protection.

    Attributes:
        token_expiry: Token expiration time in seconds (default: 3600 = 1 hour)
        cookie_name: Name of the CSRF cookie (default: "csrf_token")
        cookie_secure: Whether cookie requires HTTPS (default: True)
        cookie_httponly: Whether cookie is HTTP only (default: False, needed for JS access)
        cookie_samesite: SameSite policy for cookie (default: "lax")
        header_name: Name of the CSRF header (default: "X-CSRF-Token")
        safe_methods: HTTP methods that don't require CSRF validation
    """

    token_expiry: int = 3600
    cookie_name: str = "csrf_token"
    cookie_secure: bool = True
    cookie_httponly: bool = False  # Must be False for JS to read the cookie
    cookie_samesite: str = "lax"
    header_name: str = "X-CSRF-Token"
    safe_methods: set[str] = field(
        default_factory=lambda: {"GET", "HEAD", "OPTIONS", "TRACE"}
    )


class CSRFProtection:
    """
    CSRF protection using double-submit cookie pattern.

    Uses HMAC-SHA256 to sign tokens with a timestamp for expiration.
    Token format: {random_bytes}.{timestamp}.{signature}

    Example:
        ```python
        csrf = CSRFProtection(secret_key="your-secret-key")

        # Generate token for a form
        token = csrf.generate_token()

        # Set cookie on response
        csrf.set_cookie(response)

        # Validate token from request
        if csrf.validate_token(token):
            print("Valid token")
        ```

    Args:
        secret_key: Secret key for HMAC signing
        config: Optional CSRFConfig for customization
    """

    def __init__(
        self,
        secret_key: str,
        config: CSRFConfig | None = None,
    ):
        self.secret_key = secret_key.encode() if isinstance(secret_key, str) else secret_key
        self.config = config or CSRFConfig()
        self._current_token: str | None = None

    def generate_token(self) -> str:
        """
        Generate a new CSRF token.

        Returns:
            A signed token string in format: {random}.{timestamp}.{signature}
        """
        # Generate random bytes
        random_bytes = secrets.token_bytes(32)
        random_b64 = base64.urlsafe_b64encode(random_bytes).decode().rstrip("=")

        # Current timestamp
        timestamp = str(int(time.time()))

        # Create signature
        message = f"{random_b64}.{timestamp}"
        signature = hmac.new(
            self.secret_key,
            message.encode(),
            hashlib.sha256
        ).digest()
        signature_b64 = base64.urlsafe_b64encode(signature).decode().rstrip("=")

        token = f"{random_b64}.{timestamp}.{signature_b64}"
        self._current_token = token
        return token

    def validate_token(self, token: str) -> bool:
        """
        Validate a CSRF token.

        Checks:
        1. Token format is correct (3 parts)
        2. Signature is valid
        3. Token is not expired

        Args:
            token: The token string to validate

        Returns:
            True if token is valid, False otherwise
        """
        if not token:
            return False

        parts = token.split(".")
        if len(parts) != 3:
            return False

        random_b64, timestamp_str, signature_b64 = parts

        try:
            # Verify timestamp is not expired
            timestamp = int(timestamp_str)
            if time.time() - timestamp > self.config.token_expiry:
                return False

            # Verify signature
            message = f"{random_b64}.{timestamp_str}"
            expected_signature = hmac.new(
                self.secret_key,
                message.encode(),
                hashlib.sha256
            ).digest()
            expected_b64 = base64.urlsafe_b64encode(expected_signature).decode()
            expected_b64 = expected_b64.rstrip("=")

            return hmac.compare_digest(signature_b64, expected_b64)

        except (ValueError, TypeError):
            return False

    def set_cookie(
        self,
        response: Response,
        token: str | None = None,
    ) -> str:
        """
        Set the CSRF cookie on a response.

        Args:
            response: The response to set the cookie on
            token: Optional token to use (generates new one if not provided)

        Returns:
            The token that was set
        """
        if token is None:
            token = self.generate_token()

        response.set_cookie(
            key=self.config.cookie_name,
            value=token,
            max_age=self.config.token_expiry,
            secure=self.config.cookie_secure,
            httponly=self.config.cookie_httponly,
            samesite=self.config.cookie_samesite,
        )
        return token

    def get_token_from_request(self, request: Request) -> str | None:
        """
        Extract CSRF token from request.

        Checks header first, then form data.

        Args:
            request: The incoming request

        Returns:
            The token if found, None otherwise
        """
        # Check header first
        token = request.headers.get(self.config.header_name)
        if token:
            return token

        # Check cookie (for comparison in double-submit pattern)
        token = request.cookies.get(self.config.cookie_name)
        return token

    async def validate_request(self, request: Request) -> bool:
        """
        Validate CSRF token in a request.

        For safe methods (GET, HEAD, OPTIONS, TRACE), always returns True.
        For other methods, validates the token from header/form against cookie.

        Args:
            request: The incoming request

        Returns:
            True if valid, False otherwise
        """
        # Safe methods don't need CSRF validation
        if request.method.upper() in self.config.safe_methods:
            return True

        # Get token from header
        header_token = request.headers.get(self.config.header_name)

        # Get token from cookie
        cookie_token = request.cookies.get(self.config.cookie_name)

        if not header_token or not cookie_token:
            return False

        # In double-submit pattern, header and cookie must match
        if not hmac.compare_digest(header_token, cookie_token):
            return False

        # Validate the token itself
        return self.validate_token(header_token)


def csrf_protect(
    csrf: CSRFProtection,
    error_message: str = "CSRF validation failed",
) -> Callable[..., Any]:
    """
    Decorator factory for CSRF protection on endpoints.

    Example:
        ```python
        csrf = CSRFProtection(secret_key="your-secret-key")

        @app.post("/submit")
        @csrf_protect(csrf)
        async def submit(request: Request, data: dict):
            # This endpoint is protected
            pass
        ```

    Args:
        csrf: CSRFProtection instance
        error_message: Custom error message for validation failure

    Returns:
        Decorator function
    """
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        async def wrapper(request: Request, *args: Any, **kwargs: Any) -> Any:
            if not await csrf.validate_request(request):
                raise HTTPException(
                    status_code=403,
                    detail=error_message,
                )
            return await func(request, *args, **kwargs)

        return wrapper

    return decorator
