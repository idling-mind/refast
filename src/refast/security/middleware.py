"""Security middleware for Refast.

Provides a combined middleware that applies all security features:
- CSRF protection
- Rate limiting
- Security headers (CSP, HSTS, X-Frame-Options, etc.)

Example:
    Using SecurityMiddleware:

    ```python
    from fastapi import FastAPI
    from refast.security import SecurityMiddleware, ContentSecurityPolicy

    app = FastAPI()

    # Add with default settings
    app.add_middleware(
        SecurityMiddleware,
        secret_key="your-secret-key",
    )

    # Or with custom configuration
    csp = ContentSecurityPolicy.for_refast()

    app.add_middleware(
        SecurityMiddleware,
        secret_key="your-secret-key",
        csrf_enabled=True,
        rate_limit_enabled=True,
        rate_limit=100,
        rate_limit_window=60,
        csp=csp,
    )
    ```
"""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from refast.security.csp import ContentSecurityPolicy
from refast.security.csrf import CSRFConfig, CSRFProtection
from refast.security.rate_limit import RateLimiter

if TYPE_CHECKING:
    from starlette.types import ASGIApp


class SecurityMiddleware(BaseHTTPMiddleware):
    """
    Combined security middleware for Refast applications.

    Applies multiple security features in a single middleware:
    - CSRF protection with double-submit cookie pattern
    - Rate limiting with sliding window algorithm
    - Security headers (CSP, HSTS, X-Frame-Options, etc.)

    Example:
        ```python
        from refast.security import SecurityMiddleware

        app.add_middleware(
            SecurityMiddleware,
            secret_key="your-secret-key",
            rate_limit=100,
            rate_limit_window=60,
        )
        ```

    Args:
        app: The ASGI application
        secret_key: Secret key for CSRF token signing
        csrf_enabled: Enable CSRF protection (default: True)
        csrf_config: Custom CSRF configuration
        rate_limit_enabled: Enable rate limiting (default: True)
        rate_limit: Max requests per window (default: 100)
        rate_limit_window: Window size in seconds (default: 60)
        csp: Content Security Policy configuration
        hsts_enabled: Enable HSTS header (default: True)
        hsts_max_age: HSTS max-age in seconds (default: 1 year)
        x_content_type_options: Enable X-Content-Type-Options (default: True)
        x_frame_options: X-Frame-Options value (default: "DENY")
        x_xss_protection: Enable X-XSS-Protection (default: True)
    """

    def __init__(
        self,
        app: ASGIApp,
        secret_key: str,
        csrf_enabled: bool = True,
        csrf_config: CSRFConfig | None = None,
        rate_limit_enabled: bool = True,
        rate_limit: int = 100,
        rate_limit_window: int = 60,
        csp: ContentSecurityPolicy | None = None,
        hsts_enabled: bool = True,
        hsts_max_age: int = 31536000,
        x_content_type_options: bool = True,
        x_frame_options: str = "DENY",
        x_xss_protection: bool = True,
    ):
        super().__init__(app)

        self.secret_key = secret_key

        # CSRF protection
        self.csrf_enabled = csrf_enabled
        self.csrf: CSRFProtection | None = None
        if csrf_enabled:
            self.csrf = CSRFProtection(secret_key, csrf_config)

        # Rate limiting
        self.rate_limit_enabled = rate_limit_enabled
        self.rate_limiter: RateLimiter | None = None
        if rate_limit_enabled:
            self.rate_limiter = RateLimiter(rate_limit, rate_limit_window)

        # Content Security Policy
        self.csp = csp or ContentSecurityPolicy.for_refast()

        # Other security headers
        self.hsts_enabled = hsts_enabled
        self.hsts_max_age = hsts_max_age
        self.x_content_type_options = x_content_type_options
        self.x_frame_options = x_frame_options
        self.x_xss_protection = x_xss_protection

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Response],
    ) -> Response:
        """
        Process request with security checks.

        Order of operations:
        1. Check rate limit
        2. Process request
        3. Add security headers
        4. Set CSRF cookie on GET requests

        Args:
            request: The incoming request
            call_next: The next handler in the chain

        Returns:
            The response with security headers
        """
        # Rate limiting check
        if self.rate_limit_enabled and self.rate_limiter:
            allowed, info = await self.rate_limiter.is_allowed(request)
            if not allowed:
                return Response(
                    content="Rate limit exceeded",
                    status_code=429,
                    headers={
                        "Retry-After": str(info["reset"]),
                        "X-RateLimit-Limit": str(info["limit"]),
                        "X-RateLimit-Remaining": "0",
                        "X-RateLimit-Reset": str(info["reset"]),
                    }
                )

        # Process request
        response = await call_next(request)

        # Add security headers
        self._add_security_headers(response)

        # Set CSRF cookie on GET requests
        if self.csrf_enabled and self.csrf and request.method.upper() == "GET":
            self.csrf.set_cookie(response)

        return response

    def _add_security_headers(self, response: Response) -> None:
        """
        Add security headers to the response.

        Adds:
        - Content-Security-Policy
        - Strict-Transport-Security (HSTS)
        - X-Content-Type-Options
        - X-Frame-Options
        - X-XSS-Protection
        - Referrer-Policy

        Args:
            response: The response to add headers to
        """
        # Content Security Policy
        response.headers["Content-Security-Policy"] = self.csp.to_header()

        # HSTS (HTTP Strict Transport Security)
        if self.hsts_enabled:
            response.headers["Strict-Transport-Security"] = (
                f"max-age={self.hsts_max_age}; includeSubDomains"
            )

        # X-Content-Type-Options
        if self.x_content_type_options:
            response.headers["X-Content-Type-Options"] = "nosniff"

        # X-Frame-Options
        if self.x_frame_options:
            response.headers["X-Frame-Options"] = self.x_frame_options

        # X-XSS-Protection (legacy but still useful)
        if self.x_xss_protection:
            response.headers["X-XSS-Protection"] = "1; mode=block"

        # Referrer Policy
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # Permissions Policy (formerly Feature-Policy)
        response.headers["Permissions-Policy"] = (
            "geolocation=(), microphone=(), camera=()"
        )
