# Stage 5: Security Features

## Progress

- [ ] Task 5.1: CSRF protection
- [ ] Task 5.2: Rate limiting
- [ ] Task 5.3: Input sanitization
- [ ] Task 5.4: Content Security Policy
- [ ] Task 5.5: Security middleware
- [ ] Task 5.6: Security integration

## Objectives

Implement security features:
- CSRF protection for state-changing operations
- Rate limiting to prevent abuse
- Input sanitization to prevent XSS
- Content Security Policy headers
- Secure cookie configuration

## Prerequisites

- Stage 1 complete
- Stage 4 complete (session needed for CSRF tokens)

---

## Task 5.1: CSRF Protection

### Description
Implement CSRF protection using tokens.

### Files to Create

**src/refast/security/__init__.py**
```python
"""Security features for Refast."""

from refast.security.csrf import CSRFProtection, csrf_protect
from refast.security.rate_limit import RateLimiter, rate_limit
from refast.security.sanitizer import InputSanitizer, sanitize
from refast.security.csp import ContentSecurityPolicy

__all__ = [
    "CSRFProtection",
    "csrf_protect",
    "RateLimiter",
    "rate_limit",
    "InputSanitizer",
    "sanitize",
    "ContentSecurityPolicy",
]
```

**src/refast/security/csrf.py**
```python
"""CSRF protection."""

from typing import Any, Callable, TYPE_CHECKING
from dataclasses import dataclass
from functools import wraps
import hashlib
import hmac
import secrets
import time

from fastapi import Request, HTTPException
from fastapi.responses import Response

if TYPE_CHECKING:
    from refast.session import Session


@dataclass
class CSRFConfig:
    """CSRF protection configuration."""
    
    token_length: int = 32
    token_expiry: int = 3600  # seconds
    header_name: str = "X-CSRF-Token"
    cookie_name: str = "csrf_token"
    cookie_secure: bool = True
    cookie_httponly: bool = False  # Must be readable by JS
    cookie_samesite: str = "strict"
    exempt_methods: tuple[str, ...] = ("GET", "HEAD", "OPTIONS")


class CSRFProtection:
    """
    CSRF protection using double-submit cookie pattern.
    
    How it works:
    1. Server generates a CSRF token and stores in cookie
    2. Client sends token in header with state-changing requests
    3. Server validates header matches cookie
    
    Example:
        ```python
        csrf = CSRFProtection(secret_key="your-secret")
        
        @app.post("/api/action")
        @csrf.protect
        async def action(request: Request):
            # Protected from CSRF
            pass
        ```
    """
    
    def __init__(
        self,
        secret_key: str,
        config: CSRFConfig | None = None,
    ):
        self.secret_key = secret_key
        self.config = config or CSRFConfig()
    
    def generate_token(self) -> str:
        """Generate a new CSRF token."""
        # Generate random token
        random_bytes = secrets.token_bytes(self.config.token_length)
        timestamp = str(int(time.time())).encode()
        
        # Create HMAC signature
        message = random_bytes + timestamp
        signature = hmac.new(
            self.secret_key.encode(),
            message,
            hashlib.sha256
        ).hexdigest()
        
        # Return token: random + timestamp + signature
        return f"{random_bytes.hex()}.{timestamp.decode()}.{signature}"
    
    def validate_token(self, token: str) -> bool:
        """Validate a CSRF token."""
        try:
            parts = token.split(".")
            if len(parts) != 3:
                return False
            
            random_hex, timestamp_str, signature = parts
            random_bytes = bytes.fromhex(random_hex)
            timestamp = int(timestamp_str)
            
            # Check expiry
            if time.time() - timestamp > self.config.token_expiry:
                return False
            
            # Verify signature
            message = random_bytes + timestamp_str.encode()
            expected_signature = hmac.new(
                self.secret_key.encode(),
                message,
                hashlib.sha256
            ).hexdigest()
            
            return hmac.compare_digest(signature, expected_signature)
        except Exception:
            return False
    
    def protect(self, func: Callable) -> Callable:
        """Decorator to protect an endpoint."""
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            # Skip for exempt methods
            if request.method in self.config.exempt_methods:
                return await func(request, *args, **kwargs)
            
            # Get tokens
            cookie_token = request.cookies.get(self.config.cookie_name)
            header_token = request.headers.get(self.config.header_name)
            
            # Validate
            if not cookie_token or not header_token:
                raise HTTPException(
                    status_code=403,
                    detail="CSRF token missing"
                )
            
            if not hmac.compare_digest(cookie_token, header_token):
                raise HTTPException(
                    status_code=403,
                    detail="CSRF token mismatch"
                )
            
            if not self.validate_token(cookie_token):
                raise HTTPException(
                    status_code=403,
                    detail="CSRF token invalid or expired"
                )
            
            return await func(request, *args, **kwargs)
        
        return wrapper
    
    def set_cookie(self, response: Response, token: str | None = None) -> str:
        """Set CSRF cookie on response."""
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


def csrf_protect(secret_key: str):
    """
    Decorator factory for CSRF protection.
    
    Example:
        ```python
        @app.post("/action")
        @csrf_protect("secret-key")
        async def action(request: Request):
            pass
        ```
    """
    protection = CSRFProtection(secret_key)
    return protection.protect
```

### Tests to Write

**tests/unit/test_csrf.py**
```python
import pytest
from refast.security.csrf import CSRFProtection, CSRFConfig

class TestCSRFProtection:
    @pytest.fixture
    def csrf(self):
        return CSRFProtection(secret_key="test-secret")
    
    def test_generate_token(self, csrf):
        token = csrf.generate_token()
        assert token is not None
        assert "." in token
        parts = token.split(".")
        assert len(parts) == 3
    
    def test_validate_valid_token(self, csrf):
        token = csrf.generate_token()
        assert csrf.validate_token(token)
    
    def test_validate_invalid_token(self, csrf):
        assert not csrf.validate_token("invalid-token")
        assert not csrf.validate_token("a.b.c")
    
    def test_validate_tampered_token(self, csrf):
        token = csrf.generate_token()
        parts = token.split(".")
        # Tamper with signature
        parts[2] = "tampered"
        tampered = ".".join(parts)
        assert not csrf.validate_token(tampered)
    
    def test_tokens_are_unique(self, csrf):
        token1 = csrf.generate_token()
        token2 = csrf.generate_token()
        assert token1 != token2
```

### Acceptance Criteria

- [ ] Token generation works
- [ ] Token validation works
- [ ] Expired tokens rejected
- [ ] Tampered tokens rejected

---

## Task 5.2: Rate Limiting

### Description
Implement rate limiting to prevent abuse.

### Files to Create

**src/refast/security/rate_limit.py**
```python
"""Rate limiting."""

from typing import Callable, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from functools import wraps
from collections import defaultdict
import asyncio

from fastapi import Request, HTTPException


@dataclass
class RateLimitConfig:
    """Rate limit configuration."""
    
    max_requests: int = 100
    window_seconds: int = 60
    key_func: Callable[[Request], str] | None = None
    error_message: str = "Rate limit exceeded"


@dataclass
class RateLimitEntry:
    """Tracks requests for a key."""
    
    requests: list[datetime] = field(default_factory=list)
    
    def clean_old(self, window: timedelta) -> None:
        """Remove requests outside the window."""
        cutoff = datetime.utcnow() - window
        self.requests = [r for r in self.requests if r > cutoff]
    
    def add_request(self) -> None:
        """Record a new request."""
        self.requests.append(datetime.utcnow())
    
    @property
    def count(self) -> int:
        """Current request count."""
        return len(self.requests)


class RateLimiter:
    """
    In-memory rate limiter.
    
    Uses sliding window algorithm to limit requests per client.
    
    Example:
        ```python
        limiter = RateLimiter(max_requests=100, window_seconds=60)
        
        @app.post("/api/action")
        @limiter.limit
        async def action(request: Request):
            pass
        
        # Or with custom key
        @limiter.limit(key=lambda r: r.headers.get("API-Key"))
        async def api_action(request: Request):
            pass
        ```
    """
    
    def __init__(
        self,
        max_requests: int = 100,
        window_seconds: int = 60,
        key_func: Callable[[Request], str] | None = None,
    ):
        self.config = RateLimitConfig(
            max_requests=max_requests,
            window_seconds=window_seconds,
            key_func=key_func,
        )
        self._entries: dict[str, RateLimitEntry] = defaultdict(RateLimitEntry)
        self._lock = asyncio.Lock()
    
    def _get_key(self, request: Request) -> str:
        """Get the rate limit key for a request."""
        if self.config.key_func:
            return self.config.key_func(request)
        
        # Default: use client IP
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
        
        return request.client.host if request.client else "unknown"
    
    async def is_allowed(self, request: Request) -> tuple[bool, dict[str, Any]]:
        """
        Check if a request is allowed.
        
        Returns:
            Tuple of (allowed, info) where info contains:
            - limit: max requests allowed
            - remaining: requests remaining
            - reset: seconds until window resets
        """
        key = self._get_key(request)
        window = timedelta(seconds=self.config.window_seconds)
        
        async with self._lock:
            entry = self._entries[key]
            entry.clean_old(window)
            
            info = {
                "limit": self.config.max_requests,
                "remaining": max(0, self.config.max_requests - entry.count),
                "reset": self.config.window_seconds,
            }
            
            if entry.count >= self.config.max_requests:
                return False, info
            
            entry.add_request()
            info["remaining"] = max(0, self.config.max_requests - entry.count)
            return True, info
    
    def limit(
        self,
        func: Callable | None = None,
        *,
        key: Callable[[Request], str] | None = None,
    ) -> Callable:
        """
        Decorator to rate limit an endpoint.
        
        Can be used with or without arguments:
            @limiter.limit
            async def endpoint(): ...
            
            @limiter.limit(key=lambda r: r.headers.get("API-Key"))
            async def endpoint(): ...
        """
        def decorator(f: Callable) -> Callable:
            @wraps(f)
            async def wrapper(request: Request, *args, **kwargs):
                # Temporarily override key function if provided
                original_key_func = self.config.key_func
                if key:
                    self.config.key_func = key
                
                try:
                    allowed, info = await self.is_allowed(request)
                    
                    if not allowed:
                        raise HTTPException(
                            status_code=429,
                            detail=self.config.error_message,
                            headers={
                                "X-RateLimit-Limit": str(info["limit"]),
                                "X-RateLimit-Remaining": str(info["remaining"]),
                                "X-RateLimit-Reset": str(info["reset"]),
                                "Retry-After": str(info["reset"]),
                            }
                        )
                    
                    response = await f(request, *args, **kwargs)
                    return response
                finally:
                    self.config.key_func = original_key_func
            
            return wrapper
        
        if func is not None:
            return decorator(func)
        return decorator
    
    async def clear(self) -> None:
        """Clear all rate limit data."""
        async with self._lock:
            self._entries.clear()


def rate_limit(
    max_requests: int = 100,
    window_seconds: int = 60,
) -> Callable:
    """
    Simple rate limit decorator.
    
    Example:
        ```python
        @app.post("/action")
        @rate_limit(max_requests=10, window_seconds=60)
        async def action(request: Request):
            pass
        ```
    """
    limiter = RateLimiter(max_requests, window_seconds)
    return limiter.limit
```

### Tests to Write

**tests/unit/test_rate_limit.py**
```python
import pytest
from unittest.mock import MagicMock
from refast.security.rate_limit import RateLimiter

class TestRateLimiter:
    @pytest.fixture
    def limiter(self):
        return RateLimiter(max_requests=5, window_seconds=60)
    
    @pytest.fixture
    def mock_request(self):
        request = MagicMock()
        request.client.host = "127.0.0.1"
        request.headers = {}
        return request
    
    @pytest.mark.asyncio
    async def test_allows_under_limit(self, limiter, mock_request):
        for _ in range(5):
            allowed, _ = await limiter.is_allowed(mock_request)
            assert allowed
    
    @pytest.mark.asyncio
    async def test_blocks_over_limit(self, limiter, mock_request):
        for _ in range(5):
            await limiter.is_allowed(mock_request)
        
        allowed, info = await limiter.is_allowed(mock_request)
        assert not allowed
        assert info["remaining"] == 0
    
    @pytest.mark.asyncio
    async def test_remaining_count(self, limiter, mock_request):
        allowed, info = await limiter.is_allowed(mock_request)
        assert info["remaining"] == 4
        
        allowed, info = await limiter.is_allowed(mock_request)
        assert info["remaining"] == 3
    
    @pytest.mark.asyncio
    async def test_different_keys(self, limiter):
        request1 = MagicMock()
        request1.client.host = "1.1.1.1"
        request1.headers = {}
        
        request2 = MagicMock()
        request2.client.host = "2.2.2.2"
        request2.headers = {}
        
        # Max out request1
        for _ in range(5):
            await limiter.is_allowed(request1)
        
        # request2 should still be allowed
        allowed, _ = await limiter.is_allowed(request2)
        assert allowed
```

### Acceptance Criteria

- [ ] Rate limiting by IP works
- [ ] Custom key function works
- [ ] Sliding window algorithm works
- [ ] Returns proper headers

---

## Task 5.3: Input Sanitization

### Description
Implement input sanitization to prevent XSS.

### Files to Create

**src/refast/security/sanitizer.py**
```python
"""Input sanitization."""

from typing import Any, Callable
import html
import re
from dataclasses import dataclass
from functools import wraps

from pydantic import BaseModel, ValidationError
from fastapi import HTTPException


@dataclass
class SanitizeConfig:
    """Sanitization configuration."""
    
    strip_tags: bool = True
    escape_html: bool = True
    max_length: int | None = None
    allowed_tags: list[str] | None = None
    strip_scripts: bool = True


class InputSanitizer:
    """
    Input sanitizer for preventing XSS and other injection attacks.
    
    Example:
        ```python
        sanitizer = InputSanitizer()
        
        # Sanitize a string
        safe = sanitizer.sanitize("<script>alert('xss')</script>")
        # Returns: "&lt;script&gt;alert('xss')&lt;/script&gt;"
        
        # Sanitize form data
        data = sanitizer.sanitize_dict({
            "name": "<b>Alice</b>",
            "bio": "<script>bad()</script>Normal text",
        })
        ```
    """
    
    # Pattern for script tags
    SCRIPT_PATTERN = re.compile(
        r'<script[^>]*>.*?</script>',
        re.IGNORECASE | re.DOTALL
    )
    
    # Pattern for event handlers
    EVENT_PATTERN = re.compile(
        r'\s+on\w+\s*=\s*["\'][^"\']*["\']',
        re.IGNORECASE
    )
    
    # Pattern for javascript: URLs
    JS_URL_PATTERN = re.compile(
        r'javascript\s*:',
        re.IGNORECASE
    )
    
    def __init__(self, config: SanitizeConfig | None = None):
        self.config = config or SanitizeConfig()
    
    def sanitize(self, value: str, config: SanitizeConfig | None = None) -> str:
        """
        Sanitize a string value.
        
        Args:
            value: The input string
            config: Optional override config
            
        Returns:
            Sanitized string
        """
        cfg = config or self.config
        result = value
        
        # Strip script tags
        if cfg.strip_scripts:
            result = self.SCRIPT_PATTERN.sub('', result)
            result = self.EVENT_PATTERN.sub('', result)
            result = self.JS_URL_PATTERN.sub('', result)
        
        # Escape HTML
        if cfg.escape_html:
            result = html.escape(result)
        
        # Strip all tags
        if cfg.strip_tags:
            result = re.sub(r'<[^>]+>', '', result)
        
        # Max length
        if cfg.max_length and len(result) > cfg.max_length:
            result = result[:cfg.max_length]
        
        return result
    
    def sanitize_dict(
        self,
        data: dict[str, Any],
        config: SanitizeConfig | None = None,
    ) -> dict[str, Any]:
        """
        Recursively sanitize a dictionary.
        
        Args:
            data: Dictionary to sanitize
            config: Optional config
            
        Returns:
            Sanitized dictionary
        """
        result = {}
        
        for key, value in data.items():
            if isinstance(value, str):
                result[key] = self.sanitize(value, config)
            elif isinstance(value, dict):
                result[key] = self.sanitize_dict(value, config)
            elif isinstance(value, list):
                result[key] = [
                    self.sanitize(v, config) if isinstance(v, str)
                    else self.sanitize_dict(v, config) if isinstance(v, dict)
                    else v
                    for v in value
                ]
            else:
                result[key] = value
        
        return result
    
    @staticmethod
    def validate(
        data: dict[str, Any],
        schema: dict[str, dict[str, Any]],
    ) -> dict[str, Any]:
        """
        Validate and sanitize input against a schema.
        
        Args:
            data: Input data
            schema: Validation schema
            
        Returns:
            Validated and sanitized data
            
        Raises:
            ValueError: If validation fails
            
        Example:
            ```python
            validated = InputSanitizer.validate(
                {"email": "test@example.com", "name": "<script>"},
                schema={
                    "email": {"type": "email", "required": True},
                    "name": {"type": "string", "max_length": 100, "sanitize_html": True},
                }
            )
            ```
        """
        sanitizer = InputSanitizer()
        result = {}
        errors = []
        
        for field_name, rules in schema.items():
            value = data.get(field_name)
            
            # Check required
            if rules.get("required") and value is None:
                errors.append(f"{field_name} is required")
                continue
            
            if value is None:
                continue
            
            # Type validation
            field_type = rules.get("type", "string")
            
            if field_type == "email":
                if not re.match(r'^[^@]+@[^@]+\.[^@]+$', str(value)):
                    errors.append(f"{field_name} is not a valid email")
                    continue
            
            elif field_type == "int" or field_type == "integer":
                try:
                    value = int(value)
                except (ValueError, TypeError):
                    errors.append(f"{field_name} must be an integer")
                    continue
            
            elif field_type == "float" or field_type == "number":
                try:
                    value = float(value)
                except (ValueError, TypeError):
                    errors.append(f"{field_name} must be a number")
                    continue
            
            # String sanitization
            if isinstance(value, str):
                if rules.get("sanitize_html", True):
                    value = sanitizer.sanitize(value)
                
                max_length = rules.get("max_length")
                if max_length and len(value) > max_length:
                    value = value[:max_length]
                
                min_length = rules.get("min_length")
                if min_length and len(value) < min_length:
                    errors.append(f"{field_name} must be at least {min_length} characters")
                    continue
            
            result[field_name] = value
        
        if errors:
            raise ValueError("; ".join(errors))
        
        return result


def sanitize(func: Callable) -> Callable:
    """
    Decorator to automatically sanitize request body.
    
    Example:
        ```python
        @app.post("/submit")
        @sanitize
        async def submit(data: dict):
            # data is sanitized
            pass
        ```
    """
    sanitizer = InputSanitizer()
    
    @wraps(func)
    async def wrapper(*args, **kwargs):
        # Sanitize any dict arguments
        sanitized_kwargs = {}
        for key, value in kwargs.items():
            if isinstance(value, dict):
                sanitized_kwargs[key] = sanitizer.sanitize_dict(value)
            else:
                sanitized_kwargs[key] = value
        
        return await func(*args, **sanitized_kwargs)
    
    return wrapper
```

### Tests to Write

**tests/unit/test_sanitizer.py**
```python
import pytest
from refast.security.sanitizer import InputSanitizer, SanitizeConfig

class TestInputSanitizer:
    @pytest.fixture
    def sanitizer(self):
        return InputSanitizer()
    
    def test_escapes_html(self, sanitizer):
        result = sanitizer.sanitize("<b>bold</b>")
        assert "<" not in result or "&lt;" in result
    
    def test_removes_script_tags(self, sanitizer):
        result = sanitizer.sanitize("<script>alert('xss')</script>Hello")
        assert "script" not in result.lower()
        assert "Hello" in result or "hello" in result.lower()
    
    def test_removes_event_handlers(self, sanitizer):
        result = sanitizer.sanitize('<div onclick="evil()">Click</div>')
        assert "onclick" not in result.lower()
    
    def test_removes_javascript_urls(self, sanitizer):
        result = sanitizer.sanitize('<a href="javascript:evil()">Link</a>')
        assert "javascript:" not in result.lower()
    
    def test_sanitize_dict(self, sanitizer):
        data = {
            "name": "<script>bad</script>Alice",
            "age": 25,
            "nested": {"bio": "<b>Hello</b>"}
        }
        result = sanitizer.sanitize_dict(data)
        assert "script" not in str(result).lower()
        assert result["age"] == 25
    
    def test_validate_required(self):
        with pytest.raises(ValueError, match="email is required"):
            InputSanitizer.validate(
                {},
                {"email": {"type": "email", "required": True}}
            )
    
    def test_validate_email(self):
        result = InputSanitizer.validate(
            {"email": "test@example.com"},
            {"email": {"type": "email"}}
        )
        assert result["email"] == "test@example.com"
        
        with pytest.raises(ValueError, match="not a valid email"):
            InputSanitizer.validate(
                {"email": "not-an-email"},
                {"email": {"type": "email"}}
            )
    
    def test_max_length(self, sanitizer):
        config = SanitizeConfig(max_length=10)
        result = sanitizer.sanitize("This is a very long string", config)
        assert len(result) <= 10
```

### Acceptance Criteria

- [ ] HTML escaping works
- [ ] Script tag removal works
- [ ] Event handler removal works
- [ ] Dict sanitization works
- [ ] Schema validation works

---

## Task 5.4: Content Security Policy

### Description
Implement CSP header configuration.

### Files to Create

**src/refast/security/csp.py**
```python
"""Content Security Policy configuration."""

from typing import Any
from dataclasses import dataclass, field


@dataclass
class ContentSecurityPolicy:
    """
    Content Security Policy header configuration.
    
    CSP helps prevent XSS by controlling which resources can be loaded.
    
    Example:
        ```python
        csp = ContentSecurityPolicy(
            default_src=["'self'"],
            script_src=["'self'", "'unsafe-inline'"],
            style_src=["'self'", "'unsafe-inline'"],
            connect_src=["'self'", "wss:"],
            img_src=["'self'", "data:", "https:"],
        )
        
        # Get header value
        header = csp.to_header()
        
        # Apply to response
        response.headers["Content-Security-Policy"] = header
        ```
    """
    
    default_src: list[str] = field(default_factory=lambda: ["'self'"])
    script_src: list[str] | None = None
    style_src: list[str] | None = None
    img_src: list[str] | None = None
    font_src: list[str] | None = None
    connect_src: list[str] | None = None
    media_src: list[str] | None = None
    object_src: list[str] | None = None
    frame_src: list[str] | None = None
    frame_ancestors: list[str] | None = None
    base_uri: list[str] | None = None
    form_action: list[str] | None = None
    report_uri: str | None = None
    report_to: str | None = None
    upgrade_insecure_requests: bool = False
    block_all_mixed_content: bool = False
    
    def to_header(self) -> str:
        """Generate the CSP header value."""
        directives = []
        
        # Map attributes to directive names
        directive_map = {
            "default_src": "default-src",
            "script_src": "script-src",
            "style_src": "style-src",
            "img_src": "img-src",
            "font_src": "font-src",
            "connect_src": "connect-src",
            "media_src": "media-src",
            "object_src": "object-src",
            "frame_src": "frame-src",
            "frame_ancestors": "frame-ancestors",
            "base_uri": "base-uri",
            "form_action": "form-action",
        }
        
        for attr, directive in directive_map.items():
            value = getattr(self, attr)
            if value:
                directives.append(f"{directive} {' '.join(value)}")
        
        # Special directives
        if self.report_uri:
            directives.append(f"report-uri {self.report_uri}")
        
        if self.report_to:
            directives.append(f"report-to {self.report_to}")
        
        if self.upgrade_insecure_requests:
            directives.append("upgrade-insecure-requests")
        
        if self.block_all_mixed_content:
            directives.append("block-all-mixed-content")
        
        return "; ".join(directives)
    
    @classmethod
    def strict(cls) -> "ContentSecurityPolicy":
        """Create a strict CSP policy."""
        return cls(
            default_src=["'none'"],
            script_src=["'self'"],
            style_src=["'self'"],
            img_src=["'self'"],
            font_src=["'self'"],
            connect_src=["'self'"],
            frame_ancestors=["'none'"],
            form_action=["'self'"],
            base_uri=["'self'"],
            upgrade_insecure_requests=True,
        )
    
    @classmethod
    def for_refast(cls) -> "ContentSecurityPolicy":
        """Create a CSP policy suitable for Refast apps."""
        return cls(
            default_src=["'self'"],
            script_src=["'self'", "'unsafe-inline'"],  # Needed for React
            style_src=["'self'", "'unsafe-inline'"],
            img_src=["'self'", "data:", "https:"],
            font_src=["'self'", "https:"],
            connect_src=["'self'", "wss:", "ws:"],  # WebSocket
            frame_ancestors=["'self'"],
            form_action=["'self'"],
        )
```

### Tests to Write

**tests/unit/test_csp.py**
```python
import pytest
from refast.security.csp import ContentSecurityPolicy

class TestContentSecurityPolicy:
    def test_default_policy(self):
        csp = ContentSecurityPolicy()
        header = csp.to_header()
        assert "default-src 'self'" in header
    
    def test_multiple_directives(self):
        csp = ContentSecurityPolicy(
            default_src=["'self'"],
            script_src=["'self'", "'unsafe-inline'"],
            connect_src=["'self'", "wss:"],
        )
        header = csp.to_header()
        
        assert "default-src 'self'" in header
        assert "script-src 'self' 'unsafe-inline'" in header
        assert "connect-src 'self' wss:" in header
    
    def test_upgrade_insecure(self):
        csp = ContentSecurityPolicy(upgrade_insecure_requests=True)
        header = csp.to_header()
        assert "upgrade-insecure-requests" in header
    
    def test_strict_policy(self):
        csp = ContentSecurityPolicy.strict()
        header = csp.to_header()
        assert "default-src 'none'" in header
        assert "frame-ancestors 'none'" in header
    
    def test_refast_policy(self):
        csp = ContentSecurityPolicy.for_refast()
        header = csp.to_header()
        assert "wss:" in header  # WebSocket support
        assert "'unsafe-inline'" in header  # React support
```

### Acceptance Criteria

- [ ] CSP header generation works
- [ ] All directives supported
- [ ] Preset policies available

---

## Task 5.5: Security Middleware

### Description
Create middleware that applies all security features.

### Files to Create

**src/refast/security/middleware.py**
```python
"""Security middleware combining all security features."""

from typing import Callable, TYPE_CHECKING
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from refast.security.csrf import CSRFProtection, CSRFConfig
from refast.security.rate_limit import RateLimiter
from refast.security.csp import ContentSecurityPolicy

if TYPE_CHECKING:
    from fastapi import FastAPI


class SecurityMiddleware(BaseHTTPMiddleware):
    """
    Combined security middleware.
    
    Applies:
    - CSRF protection
    - Rate limiting
    - Security headers (CSP, etc.)
    
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
    """
    
    def __init__(
        self,
        app: "FastAPI",
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
        
        # CSRF
        self.csrf_enabled = csrf_enabled
        self.csrf = CSRFProtection(secret_key, csrf_config) if csrf_enabled else None
        
        # Rate limiting
        self.rate_limit_enabled = rate_limit_enabled
        self.rate_limiter = RateLimiter(rate_limit, rate_limit_window) if rate_limit_enabled else None
        
        # CSP
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
        call_next: Callable,
    ) -> Response:
        """Process request with security checks."""
        
        # Rate limiting
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
                    }
                )
        
        # Process request
        response = await call_next(request)
        
        # Add security headers
        self._add_security_headers(response)
        
        # Set CSRF cookie on GET requests
        if self.csrf_enabled and self.csrf and request.method == "GET":
            self.csrf.set_cookie(response)
        
        return response
    
    def _add_security_headers(self, response: Response) -> None:
        """Add security headers to response."""
        
        # Content Security Policy
        response.headers["Content-Security-Policy"] = self.csp.to_header()
        
        # HSTS
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
        
        # X-XSS-Protection
        if self.x_xss_protection:
            response.headers["X-XSS-Protection"] = "1; mode=block"
        
        # Referrer Policy
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
```

### Tests to Write

**tests/unit/test_security_middleware.py**
```python
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from refast.security.middleware import SecurityMiddleware

class TestSecurityMiddleware:
    @pytest.fixture
    def secured_app(self):
        app = FastAPI()
        app.add_middleware(
            SecurityMiddleware,
            secret_key="test-secret",
            rate_limit=5,
            rate_limit_window=60,
        )
        
        @app.get("/")
        async def home():
            return {"status": "ok"}
        
        return app
    
    def test_security_headers_present(self, secured_app):
        client = TestClient(secured_app)
        response = client.get("/")
        
        assert "Content-Security-Policy" in response.headers
        assert "X-Content-Type-Options" in response.headers
        assert "X-Frame-Options" in response.headers
    
    def test_csrf_cookie_set(self, secured_app):
        client = TestClient(secured_app)
        response = client.get("/")
        
        assert "csrf_token" in response.cookies
    
    def test_rate_limiting(self, secured_app):
        client = TestClient(secured_app)
        
        # Make 5 requests (limit)
        for _ in range(5):
            response = client.get("/")
            assert response.status_code == 200
        
        # 6th request should be rate limited
        response = client.get("/")
        assert response.status_code == 429
```

### Acceptance Criteria

- [ ] All security features combined
- [ ] Headers added correctly
- [ ] Rate limiting works
- [ ] CSRF cookie set

---

## Task 5.6: Integration with RefastApp

### Description
Integrate security features with RefastApp.

### Updates to RefastApp

```python
# In app.py

from refast.security import CSRFProtection, RateLimiter, ContentSecurityPolicy
from refast.security.middleware import SecurityMiddleware

class RefastApp:
    def __init__(
        self,
        # ... existing params
        csrf_protection: CSRFProtection | bool = True,
        rate_limiter: RateLimiter | None = None,
        csp: ContentSecurityPolicy | None = None,
    ):
        # ... existing init
        
        # Security
        if isinstance(csrf_protection, bool):
            self.csrf_protection = CSRFProtection(secret_key) if csrf_protection else None
        else:
            self.csrf_protection = csrf_protection
        
        self.rate_limiter = rate_limiter
        self.csp = csp or ContentSecurityPolicy.for_refast()
    
    def add_security_middleware(self, app: FastAPI) -> None:
        """Add security middleware to a FastAPI app."""
        app.add_middleware(
            SecurityMiddleware,
            secret_key=self.secret_key or "default-secret",
            csrf_enabled=self.csrf_protection is not None,
            rate_limit_enabled=self.rate_limiter is not None,
            csp=self.csp,
        )
```

### Acceptance Criteria

- [ ] Security configurable in RefastApp
- [ ] Middleware can be added
- [ ] Sensible defaults

---

## Final Checklist for Stage 5

- [ ] CSRF protection complete
- [ ] Rate limiting complete
- [ ] Input sanitization complete
- [ ] CSP headers complete
- [ ] Security middleware complete
- [ ] Integration complete
- [ ] All tests pass
- [ ] Update `.github/copilot-instructions.md` status to 🟢
