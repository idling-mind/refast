"""Tests for rate limiting module."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException

from refast.security.rate_limit import (
    RateLimitConfig,
    RateLimitEntry,
    RateLimiter,
    rate_limit,
)


class TestRateLimitConfig:
    """Tests for RateLimitConfig dataclass."""

    def test_default_values(self) -> None:
        """Test default configuration values."""
        config = RateLimitConfig()

        assert config.max_requests == 100
        assert config.window_seconds == 60
        assert config.key_func is None
        assert config.error_message == "Rate limit exceeded"

    def test_custom_values(self) -> None:
        """Test custom configuration values."""
        key_func = lambda r: r.headers.get("API-Key")  # noqa: E731

        config = RateLimitConfig(
            max_requests=10,
            window_seconds=30,
            key_func=key_func,
            error_message="Too many requests",
        )

        assert config.max_requests == 10
        assert config.window_seconds == 30
        assert config.key_func is key_func
        assert config.error_message == "Too many requests"


class TestRateLimitEntry:
    """Tests for RateLimitEntry dataclass."""

    def test_default_empty(self) -> None:
        """Test entry starts empty."""
        entry = RateLimitEntry()
        assert entry.count == 0
        assert entry.requests == []

    def test_add_request(self) -> None:
        """Test adding requests."""
        entry = RateLimitEntry()

        entry.add_request()
        assert entry.count == 1

        entry.add_request()
        assert entry.count == 2

    def test_clean_old_removes_expired(self) -> None:
        """Test cleaning removes old requests."""
        entry = RateLimitEntry()

        # Add old request (2 minutes ago)
        old_time = datetime.now(UTC) - timedelta(minutes=2)
        entry.requests.append(old_time)

        # Add recent request
        entry.add_request()

        assert entry.count == 2

        # Clean with 1 minute window
        entry.clean_old(timedelta(minutes=1))

        assert entry.count == 1

    def test_clean_old_keeps_recent(self) -> None:
        """Test cleaning keeps recent requests."""
        entry = RateLimitEntry()

        # Add 3 recent requests
        entry.add_request()
        entry.add_request()
        entry.add_request()

        # Clean with 1 minute window
        entry.clean_old(timedelta(minutes=1))

        assert entry.count == 3


class TestRateLimiter:
    """Tests for RateLimiter class."""

    @pytest.fixture
    def limiter(self) -> RateLimiter:
        """Create a RateLimiter for testing."""
        return RateLimiter(max_requests=5, window_seconds=60)

    @pytest.fixture
    def mock_request(self) -> MagicMock:
        """Create a mock request."""
        request = MagicMock()
        request.client.host = "127.0.0.1"
        request.headers = {}
        return request

    def test_init_default(self) -> None:
        """Test default initialization."""
        limiter = RateLimiter()
        assert limiter.config.max_requests == 100
        assert limiter.config.window_seconds == 60

    def test_init_custom(self) -> None:
        """Test custom initialization."""
        limiter = RateLimiter(max_requests=10, window_seconds=30)
        assert limiter.config.max_requests == 10
        assert limiter.config.window_seconds == 30

    def test_get_key_default(self, limiter: RateLimiter) -> None:
        """Test default key extraction (IP)."""
        request = MagicMock()
        request.client.host = "192.168.1.1"
        request.headers = {}

        key = limiter._get_key(request)
        assert key == "192.168.1.1"

    def test_get_key_forwarded(self, limiter: RateLimiter) -> None:
        """Test key extraction with X-Forwarded-For."""
        request = MagicMock()
        request.headers = {"X-Forwarded-For": "10.0.0.1, 10.0.0.2"}

        key = limiter._get_key(request)
        assert key == "10.0.0.1"

    def test_get_key_custom_func(self) -> None:
        """Test custom key function."""
        limiter = RateLimiter(key_func=lambda r: r.headers.get("API-Key", "unknown"))

        request = MagicMock()
        request.headers = {"API-Key": "my-api-key"}

        key = limiter._get_key(request)
        assert key == "my-api-key"

    def test_get_key_no_client(self, limiter: RateLimiter) -> None:
        """Test key extraction when client is None."""
        request = MagicMock()
        request.client = None
        request.headers = {}

        key = limiter._get_key(request)
        assert key == "unknown"

    @pytest.mark.asyncio
    async def test_is_allowed_under_limit(
        self, limiter: RateLimiter, mock_request: MagicMock
    ) -> None:
        """Test requests are allowed under the limit."""
        for i in range(5):
            allowed, info = await limiter.is_allowed(mock_request)
            assert allowed is True
            assert info["limit"] == 5
            assert info["remaining"] == 5 - (i + 1)

    @pytest.mark.asyncio
    async def test_is_allowed_at_limit(self, limiter: RateLimiter, mock_request: MagicMock) -> None:
        """Test request is blocked at limit."""
        # Max out requests
        for _ in range(5):
            await limiter.is_allowed(mock_request)

        # Next request should be blocked
        allowed, info = await limiter.is_allowed(mock_request)
        assert allowed is False
        assert info["remaining"] == 0
        assert info["reset"] == 60

    @pytest.mark.asyncio
    async def test_different_keys_separate_limits(self, limiter: RateLimiter) -> None:
        """Test different keys have separate rate limits."""
        request1 = MagicMock()
        request1.client.host = "1.1.1.1"
        request1.headers = {}

        request2 = MagicMock()
        request2.client.host = "2.2.2.2"
        request2.headers = {}

        # Max out request1
        for _ in range(5):
            await limiter.is_allowed(request1)

        # request1 should be blocked
        allowed1, _ = await limiter.is_allowed(request1)
        assert allowed1 is False

        # request2 should still be allowed
        allowed2, _ = await limiter.is_allowed(request2)
        assert allowed2 is True

    @pytest.mark.asyncio
    async def test_clear_resets_limits(self, limiter: RateLimiter, mock_request: MagicMock) -> None:
        """Test clearing resets all limits."""
        # Max out requests
        for _ in range(5):
            await limiter.is_allowed(mock_request)

        # Should be blocked
        allowed, _ = await limiter.is_allowed(mock_request)
        assert allowed is False

        # Clear
        await limiter.clear()

        # Should be allowed again
        allowed, _ = await limiter.is_allowed(mock_request)
        assert allowed is True

    @pytest.mark.asyncio
    async def test_get_stats(self, limiter: RateLimiter, mock_request: MagicMock) -> None:
        """Test getting rate limiter stats."""
        # Make some requests
        for _ in range(3):
            await limiter.is_allowed(mock_request)

        stats = await limiter.get_stats()

        assert stats["total_keys"] == 1
        assert stats["entries"]["127.0.0.1"] == 3


class TestRateLimiterDecorator:
    """Tests for RateLimiter.limit decorator."""

    @pytest.fixture
    def limiter(self) -> RateLimiter:
        """Create a RateLimiter for testing."""
        return RateLimiter(max_requests=3, window_seconds=60)

    @pytest.mark.asyncio
    async def test_decorator_allows_under_limit(self, limiter: RateLimiter) -> None:
        """Test decorator allows requests under limit."""
        request = MagicMock()
        request.client.host = "127.0.0.1"
        request.headers = {}

        @limiter.limit
        async def handler(request: MagicMock) -> dict[str, str]:
            return {"status": "ok"}

        result = await handler(request)
        assert result == {"status": "ok"}

    @pytest.mark.asyncio
    async def test_decorator_blocks_over_limit(self, limiter: RateLimiter) -> None:
        """Test decorator blocks requests over limit."""
        request = MagicMock()
        request.client.host = "127.0.0.1"
        request.headers = {}

        @limiter.limit
        async def handler(request: MagicMock) -> dict[str, str]:
            return {"status": "ok"}

        # Use up the limit
        for _ in range(3):
            await handler(request)

        # Next request should fail
        with pytest.raises(HTTPException) as exc_info:
            await handler(request)

        assert exc_info.value.status_code == 429
        assert "Rate limit exceeded" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_decorator_with_custom_key(self) -> None:
        """Test decorator with custom key function."""
        limiter = RateLimiter(max_requests=2, window_seconds=60)

        request1 = MagicMock()
        request1.client.host = "127.0.0.1"
        request1.headers = {"API-Key": "key-1"}

        request2 = MagicMock()
        request2.client.host = "127.0.0.1"
        request2.headers = {"API-Key": "key-2"}

        @limiter.limit(key=lambda r: r.headers.get("API-Key", "unknown"))
        async def handler(request: MagicMock) -> dict[str, str]:
            return {"status": "ok"}

        # Max out key-1
        for _ in range(2):
            await handler(request1)

        # key-1 should be blocked
        with pytest.raises(HTTPException):
            await handler(request1)

        # key-2 should still work
        result = await handler(request2)
        assert result == {"status": "ok"}

    @pytest.mark.asyncio
    async def test_rate_limit_headers(self, limiter: RateLimiter) -> None:
        """Test rate limit headers in exception."""
        request = MagicMock()
        request.client.host = "127.0.0.1"
        request.headers = {}

        @limiter.limit
        async def handler(request: MagicMock) -> dict[str, str]:
            return {"status": "ok"}

        # Max out requests
        for _ in range(3):
            await handler(request)

        with pytest.raises(HTTPException) as exc_info:
            await handler(request)

        headers = exc_info.value.headers
        assert "X-RateLimit-Limit" in headers
        assert "X-RateLimit-Remaining" in headers
        assert "X-RateLimit-Reset" in headers
        assert "Retry-After" in headers


class TestRateLimitFunction:
    """Tests for rate_limit decorator factory."""

    @pytest.mark.asyncio
    async def test_simple_rate_limit(self) -> None:
        """Test simple rate_limit decorator."""
        request = MagicMock()
        request.client.host = "127.0.0.1"
        request.headers = {}

        @rate_limit(max_requests=2, window_seconds=60)
        async def handler(request: MagicMock) -> dict[str, str]:
            return {"status": "ok"}

        # Should allow 2 requests
        result1 = await handler(request)
        assert result1 == {"status": "ok"}

        result2 = await handler(request)
        assert result2 == {"status": "ok"}

        # Third should fail
        with pytest.raises(HTTPException) as exc_info:
            await handler(request)

        assert exc_info.value.status_code == 429



