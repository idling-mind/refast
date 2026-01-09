"""Tests for Content Security Policy module."""

from __future__ import annotations

from refast.security.csp import ContentSecurityPolicy


class TestContentSecurityPolicy:
    """Tests for ContentSecurityPolicy class."""

    def test_default_policy(self) -> None:
        """Test default CSP policy."""
        csp = ContentSecurityPolicy()
        header = csp.to_header()

        assert "default-src 'self'" in header

    def test_custom_directives(self) -> None:
        """Test custom directive values."""
        csp = ContentSecurityPolicy(
            default_src=["'self'", "https:"],
            script_src=["'self'", "'unsafe-inline'"],
            style_src=["'self'", "'unsafe-inline'", "https://fonts.googleapis.com"],
        )
        header = csp.to_header()

        assert "default-src 'self' https:" in header
        assert "script-src 'self' 'unsafe-inline'" in header
        assert "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com" in header

    def test_connect_src_websocket(self) -> None:
        """Test connect-src with WebSocket support."""
        csp = ContentSecurityPolicy(
            connect_src=["'self'", "wss:", "ws:"],
        )
        header = csp.to_header()

        assert "connect-src 'self' wss: ws:" in header

    def test_img_src_data_uri(self) -> None:
        """Test img-src with data URIs."""
        csp = ContentSecurityPolicy(
            img_src=["'self'", "data:", "https:"],
        )
        header = csp.to_header()

        assert "img-src 'self' data: https:" in header

    def test_font_src(self) -> None:
        """Test font-src directive."""
        csp = ContentSecurityPolicy(
            font_src=["'self'", "https://fonts.gstatic.com"],
        )
        header = csp.to_header()

        assert "font-src 'self' https://fonts.gstatic.com" in header

    def test_media_src(self) -> None:
        """Test media-src directive."""
        csp = ContentSecurityPolicy(
            media_src=["'self'", "https://media.example.com"],
        )
        header = csp.to_header()

        assert "media-src 'self' https://media.example.com" in header

    def test_object_src(self) -> None:
        """Test object-src directive."""
        csp = ContentSecurityPolicy(
            object_src=["'none'"],
        )
        header = csp.to_header()

        assert "object-src 'none'" in header

    def test_frame_src(self) -> None:
        """Test frame-src directive."""
        csp = ContentSecurityPolicy(
            frame_src=["'self'", "https://youtube.com"],
        )
        header = csp.to_header()

        assert "frame-src 'self' https://youtube.com" in header

    def test_frame_ancestors(self) -> None:
        """Test frame-ancestors directive."""
        csp = ContentSecurityPolicy(
            frame_ancestors=["'none'"],
        )
        header = csp.to_header()

        assert "frame-ancestors 'none'" in header

    def test_base_uri(self) -> None:
        """Test base-uri directive."""
        csp = ContentSecurityPolicy(
            base_uri=["'self'"],
        )
        header = csp.to_header()

        assert "base-uri 'self'" in header

    def test_form_action(self) -> None:
        """Test form-action directive."""
        csp = ContentSecurityPolicy(
            form_action=["'self'"],
        )
        header = csp.to_header()

        assert "form-action 'self'" in header

    def test_report_uri(self) -> None:
        """Test report-uri directive."""
        csp = ContentSecurityPolicy(
            report_uri="https://example.com/csp-report",
        )
        header = csp.to_header()

        assert "report-uri https://example.com/csp-report" in header

    def test_report_to(self) -> None:
        """Test report-to directive."""
        csp = ContentSecurityPolicy(
            report_to="csp-endpoint",
        )
        header = csp.to_header()

        assert "report-to csp-endpoint" in header

    def test_upgrade_insecure_requests(self) -> None:
        """Test upgrade-insecure-requests directive."""
        csp = ContentSecurityPolicy(
            upgrade_insecure_requests=True,
        )
        header = csp.to_header()

        assert "upgrade-insecure-requests" in header

    def test_block_all_mixed_content(self) -> None:
        """Test block-all-mixed-content directive."""
        csp = ContentSecurityPolicy(
            block_all_mixed_content=True,
        )
        header = csp.to_header()

        assert "block-all-mixed-content" in header

    def test_multiple_directives_semicolon_separated(self) -> None:
        """Test that directives are semicolon-separated."""
        csp = ContentSecurityPolicy(
            default_src=["'self'"],
            script_src=["'self'"],
            style_src=["'self'"],
        )
        header = csp.to_header()

        assert ";" in header
        parts = header.split(";")
        assert len(parts) >= 3


class TestContentSecurityPolicyPresets:
    """Tests for CSP preset policies."""

    def test_strict_policy(self) -> None:
        """Test strict CSP preset."""
        csp = ContentSecurityPolicy.strict()
        header = csp.to_header()

        # Strict should use 'none' as default
        assert "default-src 'none'" in header
        # Should block framing
        assert "frame-ancestors 'none'" in header
        # Should upgrade insecure requests
        assert "upgrade-insecure-requests" in header
        # Should have 'self' for common resources
        assert "script-src 'self'" in header
        assert "style-src 'self'" in header

    def test_refast_policy(self) -> None:
        """Test Refast-optimized CSP preset."""
        csp = ContentSecurityPolicy.for_refast()
        header = csp.to_header()

        # Should allow self
        assert "default-src 'self'" in header
        # Should allow inline scripts for React
        assert "'unsafe-inline'" in header
        # Should allow WebSocket connections
        assert "wss:" in header
        assert "ws:" in header
        # Should allow data URIs for images
        assert "data:" in header

    def test_permissive_policy(self) -> None:
        """Test permissive CSP preset."""
        csp = ContentSecurityPolicy.permissive()
        header = csp.to_header()

        # Should be very permissive
        assert "'unsafe-inline'" in header
        assert "'unsafe-eval'" in header
        assert "https:" in header


class TestContentSecurityPolicyWithNonce:
    """Tests for CSP nonce support."""

    def test_with_nonce_adds_to_script_src(self) -> None:
        """Test that nonce is added to script-src."""
        csp = ContentSecurityPolicy(
            script_src=["'self'"],
        )

        new_csp = csp.with_nonce("abc123")
        header = new_csp.to_header()

        assert "'nonce-abc123'" in header
        assert "'self'" in header

    def test_with_nonce_adds_to_style_src(self) -> None:
        """Test that nonce is added to style-src."""
        csp = ContentSecurityPolicy(
            style_src=["'self'"],
        )

        new_csp = csp.with_nonce("xyz789")
        header = new_csp.to_header()

        assert "'nonce-xyz789'" in header

    def test_with_nonce_uses_default_src_if_no_script_src(self) -> None:
        """Test nonce uses default-src when script-src not set."""
        csp = ContentSecurityPolicy(
            default_src=["'self'"],
        )

        new_csp = csp.with_nonce("test123")

        # Should create script-src from default-src + nonce
        assert "'nonce-test123'" in new_csp.script_src
        assert "'self'" in new_csp.script_src

    def test_with_nonce_preserves_other_directives(self) -> None:
        """Test that with_nonce preserves other directives."""
        csp = ContentSecurityPolicy(
            default_src=["'self'"],
            img_src=["'self'", "data:"],
            connect_src=["'self'", "wss:"],
            upgrade_insecure_requests=True,
        )

        new_csp = csp.with_nonce("nonce123")
        header = new_csp.to_header()

        assert "img-src 'self' data:" in header
        assert "connect-src 'self' wss:" in header
        assert "upgrade-insecure-requests" in header

    def test_with_nonce_returns_new_instance(self) -> None:
        """Test that with_nonce returns a new instance."""
        csp = ContentSecurityPolicy()
        new_csp = csp.with_nonce("test")

        assert csp is not new_csp
        # Original should not be modified
        assert "'nonce-test'" not in csp.to_header()
        assert "'nonce-test'" in new_csp.to_header()

    def test_with_nonce_does_not_duplicate(self) -> None:
        """Test that nonce is not duplicated if already present in script-src."""
        csp = ContentSecurityPolicy(
            script_src=["'self'", "'nonce-existing'"],
            style_src=["'self'", "'nonce-existing'"],
        )

        new_csp = csp.with_nonce("existing")

        # Each directive should have nonce only once
        assert new_csp.script_src.count("'nonce-existing'") == 1
        assert new_csp.style_src.count("'nonce-existing'") == 1



