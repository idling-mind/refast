"""Tests for input sanitization module."""

from __future__ import annotations

import pytest

from refast.security.sanitizer import InputSanitizer, SanitizeConfig, sanitize


class TestSanitizeConfig:
    """Tests for SanitizeConfig dataclass."""

    def test_default_values(self) -> None:
        """Test default configuration values."""
        config = SanitizeConfig()

        assert config.strip_tags is True
        assert config.escape_html is True
        assert config.max_length is None
        assert config.allowed_tags is None
        assert config.strip_scripts is True

    def test_custom_values(self) -> None:
        """Test custom configuration values."""
        config = SanitizeConfig(
            strip_tags=False,
            escape_html=False,
            max_length=100,
            allowed_tags=["b", "i", "u"],
            strip_scripts=False,
        )

        assert config.strip_tags is False
        assert config.escape_html is False
        assert config.max_length == 100
        assert config.allowed_tags == ["b", "i", "u"]
        assert config.strip_scripts is False


class TestInputSanitizer:
    """Tests for InputSanitizer class."""

    @pytest.fixture
    def sanitizer(self) -> InputSanitizer:
        """Create an InputSanitizer instance."""
        return InputSanitizer()

    def test_init_default_config(self) -> None:
        """Test initialization with default config."""
        sanitizer = InputSanitizer()
        assert sanitizer.config is not None
        assert isinstance(sanitizer.config, SanitizeConfig)

    def test_init_custom_config(self) -> None:
        """Test initialization with custom config."""
        config = SanitizeConfig(max_length=50)
        sanitizer = InputSanitizer(config=config)
        assert sanitizer.config.max_length == 50

    def test_sanitize_plain_text(self, sanitizer: InputSanitizer) -> None:
        """Test sanitizing plain text (no changes)."""
        result = sanitizer.sanitize("Hello World")
        assert result == "Hello World"

    def test_sanitize_escapes_html(self, sanitizer: InputSanitizer) -> None:
        """Test HTML escaping."""
        result = sanitizer.sanitize("<b>bold</b>")
        # Tags should be stripped and content escaped
        assert "<" not in result or "&lt;" in result
        assert ">" not in result or "&gt;" in result

    def test_sanitize_removes_script_tags(self, sanitizer: InputSanitizer) -> None:
        """Test script tag removal."""
        result = sanitizer.sanitize("<script>alert('xss')</script>Hello")
        assert "script" not in result.lower()
        assert "alert" not in result.lower()
        assert "Hello" in result

    def test_sanitize_removes_inline_script(self, sanitizer: InputSanitizer) -> None:
        """Test inline script removal."""
        result = sanitizer.sanitize("<script type='text/javascript'>bad()</script>")
        assert "script" not in result.lower()
        assert "bad" not in result.lower()

    def test_sanitize_removes_event_handlers(self, sanitizer: InputSanitizer) -> None:
        """Test event handler removal."""
        test_cases = [
            '<div onclick="evil()">Click</div>',
            '<img onerror="evil()" src="x">',
            "<a onmouseover='evil()'>Link</a>",
            '<body onload="evil()">',
        ]

        for test in test_cases:
            result = sanitizer.sanitize(test)
            assert "onclick" not in result.lower()
            assert "onerror" not in result.lower()
            assert "onmouseover" not in result.lower()
            assert "onload" not in result.lower()

    def test_sanitize_removes_javascript_urls(self, sanitizer: InputSanitizer) -> None:
        """Test javascript: URL removal."""
        test_cases = [
            '<a href="javascript:evil()">Link</a>',
            '<a href="javascript: evil()">Link</a>',
            '<a href="JAVASCRIPT:evil()">Link</a>',
        ]

        for test in test_cases:
            result = sanitizer.sanitize(test)
            assert "javascript:" not in result.lower()

    def test_sanitize_strips_tags(self, sanitizer: InputSanitizer) -> None:
        """Test HTML tag stripping."""
        result = sanitizer.sanitize("<div><p>Hello</p></div>")
        assert "<div>" not in result
        assert "<p>" not in result
        assert "</p>" not in result
        assert "</div>" not in result

    def test_sanitize_max_length(self) -> None:
        """Test max length truncation."""
        config = SanitizeConfig(max_length=10)
        sanitizer = InputSanitizer(config=config)

        result = sanitizer.sanitize("This is a very long string")
        assert len(result) <= 10

    def test_sanitize_config_override(self, sanitizer: InputSanitizer) -> None:
        """Test config override per call."""
        override_config = SanitizeConfig(max_length=5)

        result = sanitizer.sanitize("Hello World", config=override_config)
        assert len(result) <= 5

    def test_sanitize_non_string_passthrough(self, sanitizer: InputSanitizer) -> None:
        """Test non-string values pass through unchanged."""
        result = sanitizer.sanitize(123)  # type: ignore
        assert result == 123

    def test_sanitize_dict_basic(self, sanitizer: InputSanitizer) -> None:
        """Test dictionary sanitization."""
        data = {
            "name": "<script>bad</script>Alice",
            "age": 25,
        }

        result = sanitizer.sanitize_dict(data)

        assert "script" not in str(result["name"]).lower()
        assert result["age"] == 25

    def test_sanitize_dict_nested(self, sanitizer: InputSanitizer) -> None:
        """Test nested dictionary sanitization."""
        data = {
            "user": {
                "name": "<b>Bob</b>",
                "profile": {
                    "bio": "<script>xss</script>Hello",
                },
            },
        }

        result = sanitizer.sanitize_dict(data)

        assert "script" not in str(result).lower()
        assert "Hello" in str(result)

    def test_sanitize_dict_with_lists(self, sanitizer: InputSanitizer) -> None:
        """Test dictionary with list values."""
        data = {
            "tags": ["<b>tag1</b>", "<script>bad</script>", "normal"],
            "users": [
                {"name": "<i>Alice</i>"},
                {"name": "<script>Bob</script>"},
            ],
        }

        result = sanitizer.sanitize_dict(data)

        assert "script" not in str(result).lower()
        assert len(result["tags"]) == 3
        assert len(result["users"]) == 2

    def test_sanitize_dict_preserves_non_strings(self, sanitizer: InputSanitizer) -> None:
        """Test that non-string values are preserved."""
        data = {
            "count": 42,
            "price": 19.99,
            "active": True,
            "data": None,
        }

        result = sanitizer.sanitize_dict(data)

        assert result["count"] == 42
        assert result["price"] == 19.99
        assert result["active"] is True
        assert result["data"] is None


class TestInputSanitizerValidate:
    """Tests for InputSanitizer.validate method."""

    def test_validate_required_field(self) -> None:
        """Test required field validation."""
        with pytest.raises(ValueError, match="email is required"):
            InputSanitizer.validate({}, {"email": {"type": "email", "required": True}})

    def test_validate_required_field_present(self) -> None:
        """Test required field when present."""
        result = InputSanitizer.validate(
            {"email": "test@example.com"}, {"email": {"type": "email", "required": True}}
        )
        assert result["email"] == "test@example.com"

    def test_validate_optional_field_missing(self) -> None:
        """Test optional field can be missing."""
        result = InputSanitizer.validate({}, {"name": {"type": "string", "required": False}})
        assert "name" not in result

    def test_validate_email_type(self) -> None:
        """Test email type validation."""
        # Valid email
        result = InputSanitizer.validate(
            {"email": "test@example.com"}, {"email": {"type": "email"}}
        )
        assert result["email"] == "test@example.com"

        # Invalid email
        with pytest.raises(ValueError, match="not a valid email"):
            InputSanitizer.validate({"email": "not-an-email"}, {"email": {"type": "email"}})

    def test_validate_int_type(self) -> None:
        """Test integer type validation."""
        result = InputSanitizer.validate({"age": "25"}, {"age": {"type": "int"}})
        assert result["age"] == 25
        assert isinstance(result["age"], int)

        # Also works with "integer"
        result = InputSanitizer.validate({"count": "10"}, {"count": {"type": "integer"}})
        assert result["count"] == 10

    def test_validate_int_invalid(self) -> None:
        """Test invalid integer."""
        with pytest.raises(ValueError, match="must be an integer"):
            InputSanitizer.validate({"age": "not-a-number"}, {"age": {"type": "int"}})

    def test_validate_float_type(self) -> None:
        """Test float type validation."""
        result = InputSanitizer.validate({"price": "19.99"}, {"price": {"type": "float"}})
        assert result["price"] == 19.99
        assert isinstance(result["price"], float)

        # Also works with "number"
        result = InputSanitizer.validate({"amount": "100.50"}, {"amount": {"type": "number"}})
        assert result["amount"] == 100.50

    def test_validate_float_invalid(self) -> None:
        """Test invalid float."""
        with pytest.raises(ValueError, match="must be a number"):
            InputSanitizer.validate({"price": "expensive"}, {"price": {"type": "float"}})

    def test_validate_sanitizes_strings(self) -> None:
        """Test that strings are sanitized by default."""
        result = InputSanitizer.validate(
            {"name": "<script>bad</script>Alice"}, {"name": {"type": "string"}}
        )
        assert "script" not in result["name"].lower()
        assert "Alice" in result["name"]

    def test_validate_sanitize_html_disabled(self) -> None:
        """Test disabling HTML sanitization."""
        result = InputSanitizer.validate(
            {"html": "<b>Bold</b>"}, {"html": {"type": "string", "sanitize_html": False}}
        )
        assert "<b>" in result["html"]

    def test_validate_max_length(self) -> None:
        """Test max length truncation."""
        result = InputSanitizer.validate(
            {"name": "This is a very long name"}, {"name": {"type": "string", "max_length": 10}}
        )
        assert len(result["name"]) <= 10

    def test_validate_min_length(self) -> None:
        """Test min length validation."""
        with pytest.raises(ValueError, match="at least 5 characters"):
            InputSanitizer.validate({"name": "Hi"}, {"name": {"type": "string", "min_length": 5}})

    def test_validate_multiple_errors(self) -> None:
        """Test multiple validation errors."""
        with pytest.raises(ValueError) as exc_info:
            InputSanitizer.validate(
                {},
                {
                    "email": {"type": "email", "required": True},
                    "name": {"type": "string", "required": True},
                },
            )

        error_message = str(exc_info.value)
        assert "email is required" in error_message
        assert "name is required" in error_message


class TestSanitizeDecorator:
    """Tests for sanitize decorator."""

    @pytest.mark.asyncio
    async def test_decorator_sanitizes_dict_kwargs(self) -> None:
        """Test decorator sanitizes dict arguments."""

        @sanitize
        async def handler(data: dict) -> dict:
            return data

        result = await handler(
            data={
                "name": "<script>bad</script>Alice",
            }
        )

        assert "script" not in str(result).lower()
        assert "Alice" in str(result)

    @pytest.mark.asyncio
    async def test_decorator_passes_non_dict_unchanged(self) -> None:
        """Test decorator passes non-dict values unchanged."""

        @sanitize
        async def handler(name: str, age: int) -> tuple[str, int]:
            return name, age

        result = await handler(name="Alice", age=25)
        assert result == ("Alice", 25)

    @pytest.mark.asyncio
    async def test_decorator_preserves_function_metadata(self) -> None:
        """Test decorator preserves function name and docstring."""

        @sanitize
        async def my_handler(data: dict) -> dict:
            """Handler docstring."""
            return data

        assert my_handler.__name__ == "my_handler"
        assert "Handler docstring" in my_handler.__doc__



