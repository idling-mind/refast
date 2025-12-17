"""Content Security Policy (CSP) configuration for Refast.

Provides configurable CSP headers to prevent XSS and other injection attacks
by controlling which resources can be loaded by the browser.

Example:
    Using ContentSecurityPolicy:

    ```python
    from refast.security import ContentSecurityPolicy

    # Create a custom CSP
    csp = ContentSecurityPolicy(
        default_src=["'self'"],
        script_src=["'self'", "'unsafe-inline'"],
        style_src=["'self'", "'unsafe-inline'"],
        connect_src=["'self'", "wss:"],
        img_src=["'self'", "data:", "https:"],
    )

    # Get the header value
    header = csp.to_header()
    # Returns: "default-src 'self'; script-src 'self' 'unsafe-inline'; ..."

    # Apply to response
    response.headers["Content-Security-Policy"] = header

    # Use preset policies
    strict_csp = ContentSecurityPolicy.strict()
    refast_csp = ContentSecurityPolicy.for_refast()
    ```
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ContentSecurityPolicy:
    """
    Content Security Policy header configuration.

    CSP helps prevent XSS and data injection attacks by controlling
    which resources can be loaded by the browser.

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

    Attributes:
        default_src: Default source for all resource types
        script_src: Sources for JavaScript
        style_src: Sources for CSS
        img_src: Sources for images
        font_src: Sources for fonts
        connect_src: Sources for fetch, WebSocket, EventSource
        media_src: Sources for audio/video
        object_src: Sources for object, embed, applet
        frame_src: Sources for frames
        frame_ancestors: Valid parents for embedding this page
        base_uri: Valid URLs for base element
        form_action: Valid URLs for form submissions
        report_uri: URL to send violation reports
        report_to: Reporting group name
        upgrade_insecure_requests: Upgrade HTTP to HTTPS
        block_all_mixed_content: Block all mixed content
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
        """
        Generate the CSP header value.

        Returns:
            CSP header string with all configured directives
        """
        directives: list[str] = []

        # Map Python attribute names to CSP directive names
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
    def strict(cls) -> ContentSecurityPolicy:
        """
        Create a strict CSP policy.

        This policy only allows resources from the same origin,
        blocks framing, and upgrades insecure requests.

        Returns:
            Strict ContentSecurityPolicy instance
        """
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
    def for_refast(cls) -> ContentSecurityPolicy:
        """
        Create a CSP policy suitable for Refast applications.

        This policy allows:
        - Same-origin resources
        - Inline scripts/styles (needed for React)
        - WebSocket connections
        - Data URIs for images
        - External HTTPS images and fonts

        Returns:
            ContentSecurityPolicy configured for Refast
        """
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

    @classmethod
    def permissive(cls) -> ContentSecurityPolicy:
        """
        Create a permissive CSP policy.

        Only for development - allows most resource types.
        NOT recommended for production.

        Returns:
            Permissive ContentSecurityPolicy instance
        """
        return cls(
            default_src=["'self'", "'unsafe-inline'", "'unsafe-eval'", "https:", "data:"],
            script_src=["'self'", "'unsafe-inline'", "'unsafe-eval'", "https:"],
            style_src=["'self'", "'unsafe-inline'", "https:"],
            img_src=["'self'", "data:", "https:", "http:"],
            font_src=["'self'", "https:", "data:"],
            connect_src=["'self'", "wss:", "ws:", "https:", "http:"],
        )

    def with_nonce(self, nonce: str) -> ContentSecurityPolicy:
        """
        Create a copy of this policy with a script nonce.

        Adds the nonce to script-src and style-src directives.

        Args:
            nonce: The nonce value (without 'nonce-' prefix)

        Returns:
            New ContentSecurityPolicy with nonce added
        """
        nonce_value = f"'nonce-{nonce}'"

        new_script_src = list(self.script_src or self.default_src)
        if nonce_value not in new_script_src:
            new_script_src.append(nonce_value)

        new_style_src = list(self.style_src or self.default_src)
        if nonce_value not in new_style_src:
            new_style_src.append(nonce_value)

        return ContentSecurityPolicy(
            default_src=self.default_src,
            script_src=new_script_src,
            style_src=new_style_src,
            img_src=self.img_src,
            font_src=self.font_src,
            connect_src=self.connect_src,
            media_src=self.media_src,
            object_src=self.object_src,
            frame_src=self.frame_src,
            frame_ancestors=self.frame_ancestors,
            base_uri=self.base_uri,
            form_action=self.form_action,
            report_uri=self.report_uri,
            report_to=self.report_to,
            upgrade_insecure_requests=self.upgrade_insecure_requests,
            block_all_mixed_content=self.block_all_mixed_content,
        )
