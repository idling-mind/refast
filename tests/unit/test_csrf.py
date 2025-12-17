"""Tests for CSRF protection module."""

from __future__ import annotations

import time
from unittest.mock import MagicMock

import pytest
from starlette.responses import Response

from refast.security.csrf import CSRFConfig, CSRFProtection, csrf_protect


class TestCSRFConfig:
    """Tests for CSRFConfig dataclass."""

    def test_default_values(self) -> None:
        """Test default configuration values."""
        config = CSRFConfig()

        assert config.token_expiry == 3600
        assert config.cookie_name == "csrf_token"
        assert config.cookie_secure is True
        assert config.cookie_httponly is False
        assert config.cookie_samesite == "lax"
        assert config.header_name == "X-CSRF-Token"
        assert config.safe_methods == {"GET", "HEAD", "OPTIONS", "TRACE"}

    def test_custom_values(self) -> None:
        """Test custom configuration values."""
        config = CSRFConfig(
            token_expiry=7200,
            cookie_name="my_csrf",
            cookie_secure=False,
            header_name="X-My-CSRF",
        )

        assert config.token_expiry == 7200
        assert config.cookie_name == "my_csrf"
        assert config.cookie_secure is False
        assert config.header_name == "X-My-CSRF"


class TestCSRFProtection:
    """Tests for CSRFProtection class."""

    @pytest.fixture
    def csrf(self) -> CSRFProtection:
        """Create a CSRFProtection instance for testing."""
        return CSRFProtection(secret_key="test-secret-key-12345")

    @pytest.fixture
    def csrf_short_expiry(self) -> CSRFProtection:
        """Create a CSRFProtection with short expiry for testing."""
        config = CSRFConfig(token_expiry=1)  # 1 second
        return CSRFProtection(secret_key="test-secret-key", config=config)

    def test_init_with_string_key(self) -> None:
        """Test initialization with string secret key."""
        csrf = CSRFProtection(secret_key="my-secret")
        assert csrf.secret_key == b"my-secret"

    def test_init_with_bytes_key(self) -> None:
        """Test initialization with bytes secret key."""
        csrf = CSRFProtection(secret_key=b"my-secret")
        assert csrf.secret_key == b"my-secret"

    def test_init_with_custom_config(self) -> None:
        """Test initialization with custom config."""
        config = CSRFConfig(token_expiry=7200)
        csrf = CSRFProtection(secret_key="test", config=config)
        assert csrf.config.token_expiry == 7200

    def test_generate_token(self, csrf: CSRFProtection) -> None:
        """Test token generation."""
        token = csrf.generate_token()

        assert token is not None
        assert isinstance(token, str)
        # Token format: {random}.{timestamp}.{signature}
        parts = token.split(".")
        assert len(parts) == 3

    def test_tokens_are_unique(self, csrf: CSRFProtection) -> None:
        """Test that generated tokens are unique."""
        token1 = csrf.generate_token()
        token2 = csrf.generate_token()

        assert token1 != token2

    def test_validate_valid_token(self, csrf: CSRFProtection) -> None:
        """Test validation of a valid token."""
        token = csrf.generate_token()
        assert csrf.validate_token(token) is True

    def test_validate_invalid_token(self, csrf: CSRFProtection) -> None:
        """Test validation of invalid tokens."""
        assert csrf.validate_token("") is False
        assert csrf.validate_token("invalid") is False
        assert csrf.validate_token("a.b.c") is False
        assert csrf.validate_token("not-a-real-token") is False

    def test_validate_tampered_token(self, csrf: CSRFProtection) -> None:
        """Test validation of tampered tokens."""
        token = csrf.generate_token()
        parts = token.split(".")

        # Tamper with random part
        tampered_random = "tampered" + "." + parts[1] + "." + parts[2]
        assert csrf.validate_token(tampered_random) is False

        # Tamper with timestamp
        tampered_timestamp = parts[0] + "." + "9999999999" + "." + parts[2]
        assert csrf.validate_token(tampered_timestamp) is False

        # Tamper with signature
        tampered_signature = parts[0] + "." + parts[1] + "." + "tampered"
        assert csrf.validate_token(tampered_signature) is False

    def test_validate_expired_token(self, csrf_short_expiry: CSRFProtection) -> None:
        """Test validation of expired tokens."""
        token = csrf_short_expiry.generate_token()

        # Token should be valid immediately
        assert csrf_short_expiry.validate_token(token) is True

        # Wait for expiration
        time.sleep(1.5)

        # Token should be expired
        assert csrf_short_expiry.validate_token(token) is False

    def test_validate_wrong_secret(self) -> None:
        """Test that tokens fail validation with wrong secret."""
        csrf1 = CSRFProtection(secret_key="secret-1")
        csrf2 = CSRFProtection(secret_key="secret-2")

        token = csrf1.generate_token()
        assert csrf1.validate_token(token) is True
        assert csrf2.validate_token(token) is False

    def test_set_cookie(self, csrf: CSRFProtection) -> None:
        """Test setting CSRF cookie on response."""
        response = Response()

        token = csrf.set_cookie(response)

        assert token is not None
        assert "csrf_token" in response.headers.get("set-cookie", "")

    def test_set_cookie_with_custom_token(self, csrf: CSRFProtection) -> None:
        """Test setting cookie with provided token."""
        response = Response()
        custom_token = csrf.generate_token()

        returned_token = csrf.set_cookie(response, token=custom_token)

        assert returned_token == custom_token

    def test_get_token_from_request_header(self, csrf: CSRFProtection) -> None:
        """Test extracting token from request header."""
        request = MagicMock()
        request.headers = {"X-CSRF-Token": "header-token"}
        request.cookies = {}

        token = csrf.get_token_from_request(request)
        assert token == "header-token"

    def test_get_token_from_request_cookie(self, csrf: CSRFProtection) -> None:
        """Test extracting token from cookie when header not present."""
        request = MagicMock()
        request.headers = {}
        request.cookies = {"csrf_token": "cookie-token"}

        token = csrf.get_token_from_request(request)
        assert token == "cookie-token"

    def test_get_token_header_priority(self, csrf: CSRFProtection) -> None:
        """Test that header takes priority over cookie."""
        request = MagicMock()
        request.headers = {"X-CSRF-Token": "header-token"}
        request.cookies = {"csrf_token": "cookie-token"}

        token = csrf.get_token_from_request(request)
        assert token == "header-token"

    @pytest.mark.asyncio
    async def test_validate_request_safe_methods(
        self, csrf: CSRFProtection
    ) -> None:
        """Test that safe methods pass validation."""
        for method in ["GET", "HEAD", "OPTIONS", "TRACE"]:
            request = MagicMock()
            request.method = method

            result = await csrf.validate_request(request)
            assert result is True

    @pytest.mark.asyncio
    async def test_validate_request_post_without_token(
        self, csrf: CSRFProtection
    ) -> None:
        """Test POST request fails without token."""
        request = MagicMock()
        request.method = "POST"
        request.headers = {}
        request.cookies = {}

        result = await csrf.validate_request(request)
        assert result is False

    @pytest.mark.asyncio
    async def test_validate_request_post_with_matching_tokens(
        self, csrf: CSRFProtection
    ) -> None:
        """Test POST request succeeds with matching tokens."""
        token = csrf.generate_token()

        request = MagicMock()
        request.method = "POST"
        request.headers = {"X-CSRF-Token": token}
        request.cookies = {"csrf_token": token}

        result = await csrf.validate_request(request)
        assert result is True

    @pytest.mark.asyncio
    async def test_validate_request_post_with_mismatched_tokens(
        self, csrf: CSRFProtection
    ) -> None:
        """Test POST request fails with mismatched tokens."""
        token1 = csrf.generate_token()
        token2 = csrf.generate_token()

        request = MagicMock()
        request.method = "POST"
        request.headers = {"X-CSRF-Token": token1}
        request.cookies = {"csrf_token": token2}

        result = await csrf.validate_request(request)
        assert result is False


class TestCSRFProtectDecorator:
    """Tests for csrf_protect decorator."""

    @pytest.fixture
    def csrf(self) -> CSRFProtection:
        """Create a CSRFProtection instance."""
        return CSRFProtection(secret_key="test-secret")

    @pytest.mark.asyncio
    async def test_decorator_passes_valid_request(
        self, csrf: CSRFProtection
    ) -> None:
        """Test decorator allows valid CSRF request."""
        token = csrf.generate_token()

        request = MagicMock()
        request.method = "POST"
        request.headers = {"X-CSRF-Token": token}
        request.cookies = {"csrf_token": token}

        @csrf_protect(csrf)
        async def handler(request: MagicMock) -> dict[str, str]:
            return {"status": "ok"}

        result = await handler(request)
        assert result == {"status": "ok"}

    @pytest.mark.asyncio
    async def test_decorator_blocks_invalid_request(
        self, csrf: CSRFProtection
    ) -> None:
        """Test decorator blocks invalid CSRF request."""
        from fastapi import HTTPException

        request = MagicMock()
        request.method = "POST"
        request.headers = {}
        request.cookies = {}

        @csrf_protect(csrf)
        async def handler(request: MagicMock) -> dict[str, str]:
            return {"status": "ok"}

        with pytest.raises(HTTPException) as exc_info:
            await handler(request)

        assert exc_info.value.status_code == 403
        assert "CSRF" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_decorator_custom_error_message(
        self, csrf: CSRFProtection
    ) -> None:
        """Test decorator with custom error message."""
        from fastapi import HTTPException

        request = MagicMock()
        request.method = "POST"
        request.headers = {}
        request.cookies = {}

        @csrf_protect(csrf, error_message="Custom CSRF error")
        async def handler(request: MagicMock) -> dict[str, str]:
            return {"status": "ok"}

        with pytest.raises(HTTPException) as exc_info:
            await handler(request)

        assert exc_info.value.detail == "Custom CSRF error"
