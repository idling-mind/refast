"""Tests for RefastApp class."""

from refast import RefastApp


class TestRefastApp:
    """Tests for RefastApp initialization and configuration."""

    def test_create_with_defaults(self):
        """Test RefastApp can be created with default settings."""
        app = RefastApp()
        assert app.title == "Refast App"
        assert app.debug is False
        assert app.theme is None
        assert app.secret_key is None

    def test_create_with_custom_title(self):
        """Test RefastApp can be created with a custom title."""
        app = RefastApp(title="Custom App")
        assert app.title == "Custom App"

    def test_create_with_debug_mode(self):
        """Test RefastApp can be created with debug mode enabled."""
        app = RefastApp(debug=True)
        assert app.debug is True

    def test_create_with_theme(self):
        """Test RefastApp can be created with a theme."""
        from refast.theme import Theme, ThemeColors

        theme = Theme(light=ThemeColors(primary="1 2% 3%"))
        app = RefastApp(theme=theme)
        assert app.theme is theme

    def test_create_with_secret_key(self):
        """Test RefastApp can be created with a secret key."""
        app = RefastApp(secret_key="my-secret-key")
        assert app.secret_key == "my-secret-key"


class TestPageRegistration:
    """Tests for page registration."""

    def test_page_decorator_registers_page(self):
        """Test that @page decorator registers a page."""
        app = RefastApp()

        @app.page("/")
        def home(ctx):
            return None

        assert "/" in app.pages
        assert app.pages["/"] == home

    def test_multiple_pages(self):
        """Test registering multiple pages."""
        app = RefastApp()

        @app.page("/")
        def home(ctx):
            pass

        @app.page("/about")
        def about(ctx):
            pass

        @app.page("/contact")
        def contact(ctx):
            pass

        assert len(app.pages) == 3
        assert "/" in app.pages
        assert "/about" in app.pages
        assert "/contact" in app.pages

    def test_pages_property_returns_copy(self):
        """Test that pages property returns a copy."""
        app = RefastApp()

        @app.page("/")
        def home(ctx):
            pass

        pages = app.pages
        pages["/new"] = lambda ctx: None

        assert "/new" not in app.pages


class TestEventHandlers:
    """Tests for event handler registration."""

    def test_on_event_decorator(self):
        """Test that @on_event decorator registers a handler."""
        app = RefastApp()

        @app.on_event("user:click")
        def handle_click(ctx, event):
            pass

        assert "user:click" in app._event_handlers
        assert app._event_handlers["user:click"] == handle_click

    def test_multiple_event_handlers(self):
        """Test registering multiple event handlers."""
        app = RefastApp()

        @app.on_event("user:click")
        def handle_click(ctx, event):
            pass

        @app.on_event("user:submit")
        def handle_submit(ctx, event):
            pass

        assert len(app._event_handlers) == 2


class TestCallbacks:
    """Tests for callback registration."""

    def test_register_callback(self):
        """Test registering a callback."""
        app = RefastApp()

        def my_callback():
            pass

        app.register_callback("cb-123", my_callback)
        assert app.get_callback("cb-123") == my_callback

    def test_get_callback_returns_none_for_unknown(self):
        """Test get_callback returns None for unknown ID."""
        app = RefastApp()
        assert app.get_callback("unknown") is None


class TestRouter:
    """Tests for router property."""

    def test_router_property_returns_api_router(self):
        """Test router property returns FastAPI APIRouter."""
        from fastapi import APIRouter

        app = RefastApp()
        router = app.router

        assert isinstance(router, APIRouter)

    def test_router_is_cached(self):
        """Test router is created once and cached."""
        app = RefastApp()
        router1 = app.router
        router2 = app.router

        assert router1 is router2


class TestActiveContexts:
    """Tests for active_contexts property."""

    def test_active_contexts_empty_initially(self):
        """Test active_contexts is empty initially."""
        app = RefastApp()
        assert app.active_contexts == []

    def test_active_contexts_delegates_to_router(self):
        """Test active_contexts delegates to router."""
        app = RefastApp()
        # Access router to initialize it
        _ = app.router
        assert app.active_contexts == []



