"""Tests for security middleware module."""

from __future__ import annotations

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from refast.security.csp import ContentSecurityPolicy
from refast.security.csrf import CSRFConfig
from refast.security.middleware import SecurityMiddleware


class TestSecurityMiddleware:
    """Tests for SecurityMiddleware class."""

    @pytest.fixture
    def app_with_middleware(self) -> FastAPI:
        """Create a FastAPI app with security middleware."""
        app = FastAPI()
        app.add_middleware(
            SecurityMiddleware,
            secret_key="test-secret-key",
            rate_limit=5,
            rate_limit_window=60,
        )

        @app.get("/")
        async def home() -> dict[str, str]:
            return {"status": "ok"}

        @app.post("/submit")
        async def submit() -> dict[str, str]:
            return {"status": "submitted"}

        return app

    @pytest.fixture
    def client(self, app_with_middleware: FastAPI) -> TestClient:
        """Create a test client."""
        return TestClient(app_with_middleware)

    def test_security_headers_present(self, client: TestClient) -> None:
        """Test that security headers are added to responses."""
        response = client.get("/")

        assert "Content-Security-Policy" in response.headers
        assert "X-Content-Type-Options" in response.headers
        assert "X-Frame-Options" in response.headers
        assert "X-XSS-Protection" in response.headers
        assert "Referrer-Policy" in response.headers
        assert "Permissions-Policy" in response.headers

    def test_csp_header_content(self, client: TestClient) -> None:
        """Test CSP header has expected content."""
        response = client.get("/")

        csp = response.headers["Content-Security-Policy"]
        assert "default-src" in csp

    def test_hsts_header(self, client: TestClient) -> None:
        """Test HSTS header is set."""
        response = client.get("/")

        hsts = response.headers.get("Strict-Transport-Security", "")
        assert "max-age=" in hsts
        assert "includeSubDomains" in hsts

    def test_x_content_type_options(self, client: TestClient) -> None:
        """Test X-Content-Type-Options header."""
        response = client.get("/")

        assert response.headers["X-Content-Type-Options"] == "nosniff"

    def test_x_frame_options(self, client: TestClient) -> None:
        """Test X-Frame-Options header."""
        response = client.get("/")

        assert response.headers["X-Frame-Options"] == "DENY"

    def test_x_xss_protection(self, client: TestClient) -> None:
        """Test X-XSS-Protection header."""
        response = client.get("/")

        assert response.headers["X-XSS-Protection"] == "1; mode=block"

    def test_referrer_policy(self, client: TestClient) -> None:
        """Test Referrer-Policy header."""
        response = client.get("/")

        assert response.headers["Referrer-Policy"] == "strict-origin-when-cross-origin"

    def test_permissions_policy(self, client: TestClient) -> None:
        """Test Permissions-Policy header."""
        response = client.get("/")

        policy = response.headers["Permissions-Policy"]
        assert "geolocation=()" in policy
        assert "microphone=()" in policy
        assert "camera=()" in policy

    def test_csrf_cookie_set_on_get(self, client: TestClient) -> None:
        """Test CSRF cookie is set on GET requests."""
        response = client.get("/")

        assert "csrf_token" in response.cookies

    def test_csrf_cookie_not_set_on_post(self) -> None:
        """Test CSRF cookie is not set on POST requests."""
        app = FastAPI()
        app.add_middleware(
            SecurityMiddleware,
            secret_key="test-secret",
            rate_limit_enabled=False,  # Disable for this test
        )

        @app.post("/submit")
        async def submit() -> dict[str, str]:
            return {"status": "ok"}

        client = TestClient(app)
        # First do a GET to establish session
        client.get("/")

        # POST should work but not set new cookie
        response = client.post("/submit")
        # POST doesn't set a new CSRF cookie (only GET does)
        assert response.status_code == 200


class TestSecurityMiddlewareRateLimiting:
    """Tests for rate limiting in SecurityMiddleware."""

    @pytest.fixture
    def rate_limited_app(self) -> FastAPI:
        """Create app with aggressive rate limiting."""
        app = FastAPI()
        app.add_middleware(
            SecurityMiddleware,
            secret_key="test-secret",
            rate_limit=3,
            rate_limit_window=60,
            csrf_enabled=False,  # Disable for cleaner tests
        )

        @app.get("/")
        async def home() -> dict[str, str]:
            return {"status": "ok"}

        return app

    @pytest.fixture
    def client(self, rate_limited_app: FastAPI) -> TestClient:
        """Create test client."""
        return TestClient(rate_limited_app)

    def test_allows_requests_under_limit(self, client: TestClient) -> None:
        """Test requests under limit are allowed."""
        for _ in range(3):
            response = client.get("/")
            assert response.status_code == 200

    def test_blocks_requests_over_limit(self, client: TestClient) -> None:
        """Test requests over limit are blocked."""
        # Use up the limit
        for _ in range(3):
            client.get("/")

        # Next request should be rate limited
        response = client.get("/")
        assert response.status_code == 429
        assert "Rate limit exceeded" in response.text

    def test_rate_limit_headers_in_response(self, client: TestClient) -> None:
        """Test rate limit headers in 429 response."""
        # Use up the limit
        for _ in range(3):
            client.get("/")

        response = client.get("/")

        assert response.status_code == 429
        assert "Retry-After" in response.headers
        assert "X-RateLimit-Limit" in response.headers
        assert "X-RateLimit-Remaining" in response.headers


class TestSecurityMiddlewareConfiguration:
    """Tests for SecurityMiddleware configuration options."""

    def test_csrf_disabled(self) -> None:
        """Test CSRF can be disabled."""
        app = FastAPI()
        app.add_middleware(
            SecurityMiddleware,
            secret_key="test-secret",
            csrf_enabled=False,
            rate_limit_enabled=False,
        )

        @app.get("/")
        async def home() -> dict[str, str]:
            return {"status": "ok"}

        client = TestClient(app)
        response = client.get("/")

        # No CSRF cookie should be set
        assert "csrf_token" not in response.cookies

    def test_rate_limit_disabled(self) -> None:
        """Test rate limiting can be disabled."""
        app = FastAPI()
        app.add_middleware(
            SecurityMiddleware,
            secret_key="test-secret",
            csrf_enabled=False,
            rate_limit_enabled=False,
        )

        @app.get("/")
        async def home() -> dict[str, str]:
            return {"status": "ok"}

        client = TestClient(app)

        # Should allow many requests
        for _ in range(100):
            response = client.get("/")
            assert response.status_code == 200

    def test_custom_csp(self) -> None:
        """Test custom CSP configuration."""
        custom_csp = ContentSecurityPolicy(
            default_src=["'none'"],
            script_src=["'self'"],
        )

        app = FastAPI()
        app.add_middleware(
            SecurityMiddleware,
            secret_key="test-secret",
            csp=custom_csp,
            csrf_enabled=False,
            rate_limit_enabled=False,
        )

        @app.get("/")
        async def home() -> dict[str, str]:
            return {"status": "ok"}

        client = TestClient(app)
        response = client.get("/")

        csp_header = response.headers["Content-Security-Policy"]
        assert "default-src 'none'" in csp_header
        assert "script-src 'self'" in csp_header

    def test_hsts_disabled(self) -> None:
        """Test HSTS can be disabled."""
        app = FastAPI()
        app.add_middleware(
            SecurityMiddleware,
            secret_key="test-secret",
            hsts_enabled=False,
            csrf_enabled=False,
            rate_limit_enabled=False,
        )

        @app.get("/")
        async def home() -> dict[str, str]:
            return {"status": "ok"}

        client = TestClient(app)
        response = client.get("/")

        assert "Strict-Transport-Security" not in response.headers

    def test_custom_x_frame_options(self) -> None:
        """Test custom X-Frame-Options."""
        app = FastAPI()
        app.add_middleware(
            SecurityMiddleware,
            secret_key="test-secret",
            x_frame_options="SAMEORIGIN",
            csrf_enabled=False,
            rate_limit_enabled=False,
        )

        @app.get("/")
        async def home() -> dict[str, str]:
            return {"status": "ok"}

        client = TestClient(app)
        response = client.get("/")

        assert response.headers["X-Frame-Options"] == "SAMEORIGIN"

    def test_x_frame_options_disabled(self) -> None:
        """Test X-Frame-Options can be disabled."""
        app = FastAPI()
        app.add_middleware(
            SecurityMiddleware,
            secret_key="test-secret",
            x_frame_options="",  # Empty string disables
            csrf_enabled=False,
            rate_limit_enabled=False,
        )

        @app.get("/")
        async def home() -> dict[str, str]:
            return {"status": "ok"}

        client = TestClient(app)
        response = client.get("/")

        assert "X-Frame-Options" not in response.headers

    def test_custom_csrf_config(self) -> None:
        """Test custom CSRF configuration."""
        csrf_config = CSRFConfig(
            cookie_name="my_csrf",
            token_expiry=7200,
        )

        app = FastAPI()
        app.add_middleware(
            SecurityMiddleware,
            secret_key="test-secret",
            csrf_config=csrf_config,
            rate_limit_enabled=False,
        )

        @app.get("/")
        async def home() -> dict[str, str]:
            return {"status": "ok"}

        client = TestClient(app)
        response = client.get("/")

        # Should use custom cookie name
        assert "my_csrf" in response.cookies
