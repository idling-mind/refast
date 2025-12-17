"""Rate limiting for Refast.

Provides in-memory rate limiting using a sliding window algorithm
to prevent abuse and control API usage.

Example:
    Using RateLimiter:

    ```python
    from refast.security import RateLimiter, rate_limit
    from fastapi import FastAPI, Request

    app = FastAPI()

    # Create a rate limiter
    limiter = RateLimiter(max_requests=100, window_seconds=60)

    # Use as decorator
    @app.post("/api/action")
    @limiter.limit
    async def action(request: Request):
        return {"status": "ok"}

    # Or with custom key function
    @app.post("/api/premium")
    @limiter.limit(key=lambda r: r.headers.get("API-Key"))
    async def premium_action(request: Request):
        return {"status": "ok"}

    # Simple one-off decorator
    @app.post("/api/simple")
    @rate_limit(max_requests=10, window_seconds=60)
    async def simple_action(request: Request):
        return {"status": "ok"}
    ```
"""

from __future__ import annotations

import asyncio
from collections import defaultdict
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from functools import wraps
from typing import TYPE_CHECKING, Any

from fastapi import HTTPException, Request

if TYPE_CHECKING:
    pass


@dataclass
class RateLimitConfig:
    """
    Rate limit configuration.

    Attributes:
        max_requests: Maximum number of requests allowed in the window
        window_seconds: Time window in seconds
        key_func: Optional function to extract rate limit key from request
        error_message: Error message when rate limit is exceeded
    """

    max_requests: int = 100
    window_seconds: int = 60
    key_func: Callable[[Request], str] | None = None
    error_message: str = "Rate limit exceeded"


@dataclass
class RateLimitEntry:
    """
    Tracks requests for a specific key.

    Maintains a list of request timestamps to implement sliding window.

    Attributes:
        requests: List of request timestamps
    """

    requests: list[datetime] = field(default_factory=list)

    def clean_old(self, window: timedelta) -> None:
        """
        Remove requests outside the time window.

        Args:
            window: The time window as a timedelta
        """
        cutoff = datetime.now(UTC) - window
        self.requests = [r for r in self.requests if r > cutoff]

    def add_request(self) -> None:
        """Record a new request with current timestamp."""
        self.requests.append(datetime.now(UTC))

    @property
    def count(self) -> int:
        """Current request count in the window."""
        return len(self.requests)


class RateLimiter:
    """
    In-memory rate limiter using sliding window algorithm.

    Limits requests per client based on IP address or custom key function.
    Thread-safe using asyncio locks.

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

        # Check manually
        allowed, info = await limiter.is_allowed(request)
        if not allowed:
            print(f"Rate limited. Retry after {info['reset']} seconds")
        ```

    Args:
        max_requests: Maximum requests allowed in window
        window_seconds: Time window in seconds
        key_func: Optional function to extract key from request
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
        """
        Get the rate limit key for a request.

        Uses custom key function if provided, otherwise extracts client IP.

        Args:
            request: The incoming request

        Returns:
            Rate limit key string
        """
        if self.config.key_func:
            return self.config.key_func(request)

        # Default: use client IP
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()

        return request.client.host if request.client else "unknown"

    async def is_allowed(self, request: Request) -> tuple[bool, dict[str, Any]]:
        """
        Check if a request is allowed under the rate limit.

        Args:
            request: The incoming request

        Returns:
            Tuple of (allowed, info) where info contains:
            - limit: Maximum requests allowed
            - remaining: Requests remaining in window
            - reset: Seconds until window resets
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
        func: Callable[..., Any] | None = None,
        *,
        key: Callable[[Request], str] | None = None,
    ) -> Callable[..., Any]:
        """
        Decorator to rate limit an endpoint.

        Can be used with or without arguments:

            @limiter.limit
            async def endpoint(): ...

            @limiter.limit(key=lambda r: r.headers.get("API-Key"))
            async def endpoint(): ...

        Args:
            func: The function to wrap (when used without parentheses)
            key: Optional custom key function for this endpoint

        Returns:
            Decorated function or decorator
        """
        def decorator(f: Callable[..., Any]) -> Callable[..., Any]:
            @wraps(f)
            async def wrapper(request: Request, *args: Any, **kwargs: Any) -> Any:
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

                    return await f(request, *args, **kwargs)
                finally:
                    self.config.key_func = original_key_func

            return wrapper

        if func is not None:
            return decorator(func)
        return decorator

    async def clear(self) -> None:
        """Clear all rate limit entries."""
        async with self._lock:
            self._entries.clear()

    async def get_stats(self) -> dict[str, Any]:
        """
        Get current rate limiter statistics.

        Returns:
            Dictionary with:
            - total_keys: Number of tracked keys
            - entries: Dictionary of key -> request count
        """
        async with self._lock:
            return {
                "total_keys": len(self._entries),
                "entries": {k: v.count for k, v in self._entries.items()},
            }


def rate_limit(
    max_requests: int = 100,
    window_seconds: int = 60,
) -> Callable[..., Any]:
    """
    Simple rate limit decorator factory.

    Creates a new RateLimiter for each decorated function.
    For shared rate limiting across endpoints, use RateLimiter class directly.

    Example:
        ```python
        @app.post("/action")
        @rate_limit(max_requests=10, window_seconds=60)
        async def action(request: Request):
            return {"status": "ok"}
        ```

    Args:
        max_requests: Maximum requests allowed in window
        window_seconds: Time window in seconds

    Returns:
        Decorator function
    """
    limiter = RateLimiter(max_requests, window_seconds)
    return limiter.limit
