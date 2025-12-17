"""Security features for Refast.

This module provides comprehensive security features including:
- CSRF protection
- Rate limiting
- Input sanitization
- Content Security Policy (CSP)
- Combined security middleware

Example:
    Basic usage with RefastApp:

    ```python
    from refast import RefastApp
    from refast.security import (
        CSRFProtection,
        RateLimiter,
        ContentSecurityPolicy,
        SecurityMiddleware,
    )

    # Create app with security
    app = RefastApp(
        secret_key="your-secret-key",
    )

    # Custom CSP
    csp = ContentSecurityPolicy.for_refast()

    # Add security middleware
    app.add_middleware(
        SecurityMiddleware,
        secret_key="your-secret-key",
        csp=csp,
    )
    ```
"""

from refast.security.csp import ContentSecurityPolicy  # noqa: F401
from refast.security.csrf import (  # noqa: F401
    CSRFConfig,
    CSRFProtection,
    csrf_protect,
)
from refast.security.middleware import SecurityMiddleware  # noqa: F401
from refast.security.rate_limit import (  # noqa: F401
    RateLimitConfig,
    RateLimitEntry,
    RateLimiter,
    rate_limit,
)
from refast.security.sanitizer import (  # noqa: F401
    InputSanitizer,
    SanitizeConfig,
    sanitize,
)

__all__ = [
    # CSRF
    "CSRFProtection",
    "CSRFConfig",
    "csrf_protect",
    # Rate limiting
    "RateLimiter",
    "RateLimitConfig",
    "RateLimitEntry",
    "rate_limit",
    # Sanitization
    "InputSanitizer",
    "SanitizeConfig",
    "sanitize",
    # CSP
    "ContentSecurityPolicy",
    # Middleware
    "SecurityMiddleware",
]
