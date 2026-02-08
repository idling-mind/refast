"""Security — /docs/advanced/security."""

from refast.components import Container, Heading, Markdown, Separator


PAGE_TITLE = "Security"
PAGE_ROUTE = "/docs/advanced/security"


def render(ctx):
    """Render the security guide page."""
    from docs_site.app import docs_layout

    content = Container(
        class_name="max-w-4xl mx-auto p-6",
        children=[
            Heading(PAGE_TITLE, level=1),
            Separator(class_name="my-4"),
            Markdown(content=CONTENT),
        ],
    )
    return docs_layout(ctx, content, PAGE_ROUTE)


CONTENT = r"""
> **TODO**: This page needs full content. See `AGENT_INSTRUCTIONS.md` in this folder.

## Overview

Refast includes built-in security features: CSRF protection, rate limiting, input
sanitization, and Content Security Policy headers.

## SecurityMiddleware

The all-in-one middleware that combines all security features:

```python
from refast.security import SecurityMiddleware

middleware = SecurityMiddleware(
    secret_key="your-secret-key",
    rate_limit=100,           # requests per window
    rate_window=60,           # window in seconds
    enable_csrf=True,
    enable_sanitization=True,
    enable_csp=True,
)
```

## CSRF Protection

Double-submit cookie pattern with HMAC-SHA256 signed tokens:

```python
from refast.security import CSRFProtection

csrf = CSRFProtection(secret_key="secret")
token = csrf.generate_token(session_id)
csrf.validate_token(token, session_id)  # raises on invalid
```

## Rate Limiting

Sliding window rate limiter per client:

```python
from refast.security import RateLimiter

limiter = RateLimiter(max_requests=100, window_seconds=60)
allowed = await limiter.check("client-ip")
```

## Input Sanitization

Removes script tags, event handlers, and `javascript:` URLs:

```python
from refast.security import InputSanitizer

sanitizer = InputSanitizer()
clean = sanitizer.sanitize("<script>alert('xss')</script>Hello")
# Returns: "Hello"
```

## Content Security Policy

```python
from refast.security import ContentSecurityPolicy

csp = ContentSecurityPolicy.for_refast()  # Preset for Refast apps
header_value = csp.to_header()
```

## Next Steps

- [Sessions](/docs/advanced/sessions) — Server-side session management
- [Styling](/docs/advanced/styling) — CSS and Tailwind patterns
"""
