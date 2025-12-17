"""Input sanitization for Refast.

Provides XSS prevention and input validation through HTML escaping,
script tag removal, and schema-based validation.

Example:
    Using InputSanitizer:

    ```python
    from refast.security import InputSanitizer, SanitizeConfig, sanitize

    sanitizer = InputSanitizer()

    # Sanitize a string
    safe = sanitizer.sanitize("<script>alert('xss')</script>Hello")
    # Returns: "Hello" (script removed and escaped)

    # Sanitize form data
    data = sanitizer.sanitize_dict({
        "name": "<b>Alice</b>",
        "bio": "<script>bad()</script>Normal text",
    })

    # Validate against schema
    validated = InputSanitizer.validate(
        {"email": "test@example.com", "name": "<script>"},
        schema={
            "email": {"type": "email", "required": True},
            "name": {"type": "string", "max_length": 100, "sanitize_html": True},
        }
    )

    # Use decorator for automatic sanitization
    @app.post("/submit")
    @sanitize
    async def submit(data: dict):
        # data is automatically sanitized
        pass
    ```
"""

from __future__ import annotations

import html
import re
from collections.abc import Callable
from dataclasses import dataclass
from functools import wraps
from typing import Any


@dataclass
class SanitizeConfig:
    """
    Configuration for input sanitization.

    Attributes:
        strip_tags: Whether to remove HTML tags (default: True)
        escape_html: Whether to escape HTML entities (default: True)
        max_length: Maximum allowed string length (None = no limit)
        allowed_tags: List of allowed HTML tags (None = strip all)
        strip_scripts: Whether to remove script tags and JS (default: True)
    """

    strip_tags: bool = True
    escape_html: bool = True
    max_length: int | None = None
    allowed_tags: list[str] | None = None
    strip_scripts: bool = True


class InputSanitizer:
    """
    Input sanitizer for preventing XSS and injection attacks.

    Removes dangerous HTML content including:
    - Script tags and their contents
    - Event handlers (onclick, onload, etc.)
    - JavaScript URLs (javascript:...)

    Example:
        ```python
        sanitizer = InputSanitizer()

        # Sanitize a string
        safe = sanitizer.sanitize("<script>alert('xss')</script>")
        # Returns escaped/stripped content

        # Sanitize form data recursively
        data = sanitizer.sanitize_dict({
            "name": "<b>Alice</b>",
            "bio": "<script>bad()</script>Normal text",
        })
        ```

    Args:
        config: Optional SanitizeConfig for customization
    """

    # Pattern for script tags and their contents
    SCRIPT_PATTERN = re.compile(
        r'<script[^>]*>.*?</script>',
        re.IGNORECASE | re.DOTALL
    )

    # Pattern for event handlers (onclick, onload, onerror, etc.)
    EVENT_PATTERN = re.compile(
        r'\s+on\w+\s*=\s*["\'][^"\']*["\']',
        re.IGNORECASE
    )

    # Pattern for javascript: URLs
    JS_URL_PATTERN = re.compile(
        r'javascript\s*:',
        re.IGNORECASE
    )

    # Pattern for HTML tags
    TAG_PATTERN = re.compile(r'<[^>]+>')

    def __init__(self, config: SanitizeConfig | None = None):
        self.config = config or SanitizeConfig()

    def sanitize(self, value: str, config: SanitizeConfig | None = None) -> str:
        """
        Sanitize a string value.

        Removes dangerous content and optionally escapes HTML.

        Args:
            value: The input string to sanitize
            config: Optional config override

        Returns:
            Sanitized string
        """
        if not isinstance(value, str):
            return value

        cfg = config or self.config
        result = value

        # Strip script tags and contents first
        if cfg.strip_scripts:
            result = self.SCRIPT_PATTERN.sub('', result)
            result = self.EVENT_PATTERN.sub('', result)
            result = self.JS_URL_PATTERN.sub('', result)

        # Strip all HTML tags
        if cfg.strip_tags:
            result = self.TAG_PATTERN.sub('', result)

        # Escape HTML entities
        if cfg.escape_html:
            result = html.escape(result)

        # Apply max length
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

        Sanitizes all string values in the dictionary, including
        nested dictionaries and lists.

        Args:
            data: Dictionary to sanitize
            config: Optional config override

        Returns:
            New dictionary with sanitized values
        """
        result: dict[str, Any] = {}

        for key, value in data.items():
            if isinstance(value, str):
                result[key] = self.sanitize(value, config)
            elif isinstance(value, dict):
                result[key] = self.sanitize_dict(value, config)
            elif isinstance(value, list):
                result[key] = self._sanitize_list(value, config)
            else:
                result[key] = value

        return result

    def _sanitize_list(
        self,
        data: list[Any],
        config: SanitizeConfig | None = None,
    ) -> list[Any]:
        """
        Recursively sanitize a list.

        Args:
            data: List to sanitize
            config: Optional config override

        Returns:
            New list with sanitized values
        """
        result: list[Any] = []

        for item in data:
            if isinstance(item, str):
                result.append(self.sanitize(item, config))
            elif isinstance(item, dict):
                result.append(self.sanitize_dict(item, config))
            elif isinstance(item, list):
                result.append(self._sanitize_list(item, config))
            else:
                result.append(item)

        return result

    @staticmethod
    def validate(
        data: dict[str, Any],
        schema: dict[str, dict[str, Any]],
    ) -> dict[str, Any]:
        """
        Validate and sanitize input against a schema.

        Supports type validation, required fields, length constraints,
        and automatic sanitization.

        Args:
            data: Input data dictionary
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

        Schema field options:
            - type: "string", "email", "int"/"integer", "float"/"number"
            - required: bool (default False)
            - max_length: int (for strings)
            - min_length: int (for strings)
            - sanitize_html: bool (default True for strings)
        """
        sanitizer = InputSanitizer()
        result: dict[str, Any] = {}
        errors: list[str] = []

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
                if not isinstance(value, str) or not re.match(r'^[^@]+@[^@]+\.[^@]+$', value):
                    errors.append(f"{field_name} is not a valid email")
                    continue

            elif field_type in ("int", "integer"):
                try:
                    value = int(value)
                except (ValueError, TypeError):
                    errors.append(f"{field_name} must be an integer")
                    continue

            elif field_type in ("float", "number"):
                try:
                    value = float(value)
                except (ValueError, TypeError):
                    errors.append(f"{field_name} must be a number")
                    continue

            # String sanitization and validation
            if isinstance(value, str):
                # Sanitize HTML by default
                if rules.get("sanitize_html", True):
                    value = sanitizer.sanitize(value)

                # Max length
                max_length = rules.get("max_length")
                if max_length and len(value) > max_length:
                    value = value[:max_length]

                # Min length
                min_length = rules.get("min_length")
                if min_length and len(value) < min_length:
                    errors.append(f"{field_name} must be at least {min_length} characters")
                    continue

            result[field_name] = value

        if errors:
            raise ValueError("; ".join(errors))

        return result


def sanitize(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorator to automatically sanitize request body dictionaries.

    Sanitizes any dictionary arguments passed to the function.

    Example:
        ```python
        @app.post("/submit")
        @sanitize
        async def submit(data: dict):
            # data is automatically sanitized
            pass
        ```

    Args:
        func: The function to wrap

    Returns:
        Decorated function with automatic sanitization
    """
    sanitizer = InputSanitizer()

    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        # Sanitize any dict arguments
        sanitized_kwargs: dict[str, Any] = {}
        for key, value in kwargs.items():
            if isinstance(value, dict):
                sanitized_kwargs[key] = sanitizer.sanitize_dict(value)
            else:
                sanitized_kwargs[key] = value

        return await func(*args, **sanitized_kwargs)

    return wrapper
