"""Tests for RefastApp class."""

import pytest

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
    """Tests for callback registration — callbacks live on Context, not RefastApp."""

    def test_callback_registers_on_context(self):
        """Callbacks are registered on the Context that created them."""
        from refast.context import Context

        ctx = Context()

        def my_callback():
            pass

        cb = ctx.callback(my_callback)
        assert ctx.get_callback(cb.id) == my_callback

    def test_callback_not_visible_on_sibling_context(self):
        """A callback registered on one Context is not visible on another."""
        from refast.context import Context

        ctx1 = Context()
        ctx2 = Context()

        def my_callback():
            pass

        cb = ctx1.callback(my_callback)
        assert ctx1.get_callback(cb.id) == my_callback
        assert ctx2.get_callback(cb.id) is None

    def test_clear_callbacks_removes_all(self):
        """clear_callbacks discards all registered callbacks."""
        from refast.context import Context

        ctx = Context()

        def my_callback():
            pass

        ctx.callback(my_callback)
        ctx.callback(my_callback)
        ctx.clear_callbacks()
        assert ctx._callbacks == {}

    def test_get_callback_returns_none_for_unknown(self):
        """get_callback returns None for an unknown ID."""
        from refast.context import Context

        ctx = Context()
        assert ctx.get_callback("unknown-id") is None


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


class TestRouteMatching:
    """Tests for RefastApp.match_route() and path-parameter routing."""

    # ------------------------------------------------------------------ #
    # Exact (static) routes                                                #
    # ------------------------------------------------------------------ #

    def test_exact_route_matched(self):
        """Exact-path routes are returned by match_route."""
        app = RefastApp()

        @app.page("/")
        def home(ctx):
            pass

        func, params = app.match_route("/")
        assert func is home
        assert params == {}

    def test_exact_route_unmatched_returns_none(self):
        """match_route returns (None, {}) for unknown paths."""
        app = RefastApp()
        func, params = app.match_route("/does-not-exist")
        assert func is None
        assert params == {}

    def test_exact_has_priority_over_pattern(self):
        """Exact routes take priority over parameterised ones with same structure."""
        app = RefastApp()

        @app.page("/users/me")
        def me(ctx):
            pass

        @app.page("/users/{id}")
        def user(ctx):
            pass

        func, params = app.match_route("/users/me")
        assert func is me
        assert params == {}

    # ------------------------------------------------------------------ #
    # Path parameters — basic                                              #
    # ------------------------------------------------------------------ #

    def test_single_str_param(self):
        """Single string path parameter is extracted."""
        app = RefastApp()

        @app.page("/users/{username}")
        def user(ctx):
            pass

        func, params = app.match_route("/users/alice")
        assert func is user
        assert params == {"username": "alice"}

    def test_multiple_str_params(self):
        """Multiple string path parameters are all extracted."""
        app = RefastApp()

        @app.page("/posts/{year}/{slug}")
        def post(ctx):
            pass

        func, params = app.match_route("/posts/2025/hello-world")
        assert func is post
        assert params == {"year": "2025", "slug": "hello-world"}

    def test_pattern_does_not_match_wrong_path(self):
        """A parameterised pattern does not match a path with wrong prefix."""
        app = RefastApp()

        @app.page("/users/{id}")
        def user(ctx):
            pass

        func, params = app.match_route("/posts/42")
        assert func is None

    def test_param_does_not_match_extra_segments(self):
        """A single-segment param does not swallow extra slashes."""
        app = RefastApp()

        @app.page("/users/{id}")
        def user(ctx):
            pass

        func, params = app.match_route("/users/42/extra")
        assert func is None

    # ------------------------------------------------------------------ #
    # Type coercion                                                         #
    # ------------------------------------------------------------------ #

    def test_int_param_coerced(self):
        """An {id:int} parameter is coerced to an int."""
        app = RefastApp()

        @app.page("/items/{id:int}")
        def item(ctx):
            pass

        func, params = app.match_route("/items/99")
        assert func is item
        assert params["id"] == 99
        assert isinstance(params["id"], int)

    def test_int_param_only_matches_digits(self):
        """An {id:int} route does not match a non-numeric segment."""
        app = RefastApp()

        @app.page("/items/{id:int}")
        def item(ctx):
            pass

        func, params = app.match_route("/items/abc")
        assert func is None

    def test_float_param_coerced(self):
        """A {value:float} parameter is coerced to a float."""
        app = RefastApp()

        @app.page("/data/{value:float}")
        def data(ctx):
            pass

        func, params = app.match_route("/data/3.14")
        assert func is data
        assert params["value"] == pytest.approx(3.14)
        assert isinstance(params["value"], float)

    def test_uuid_param_matched(self):
        """A {id:uuid} param matches a valid UUID string."""
        app = RefastApp()
        uid = "123e4567-e89b-12d3-a456-426614174000"

        @app.page("/docs/{id:uuid}")
        def doc(ctx):
            pass

        func, params = app.match_route(f"/docs/{uid}")
        assert func is doc
        assert params["id"] == uid

    def test_uuid_param_rejects_non_uuid(self):
        """A {id:uuid} route does not match a non-UUID string."""
        app = RefastApp()

        @app.page("/docs/{id:uuid}")
        def doc(ctx):
            pass

        func, params = app.match_route("/docs/not-a-uuid")
        assert func is None

    # ------------------------------------------------------------------ #
    # Registration order                                                   #
    # ------------------------------------------------------------------ #

    def test_first_registered_pattern_wins(self):
        """When two patterns match, the first registered is returned."""
        app = RefastApp()

        @app.page("/a/{x}")
        def first(ctx):
            pass

        @app.page("/a/{y}")
        def second(ctx):
            pass

        func, _ = app.match_route("/a/hello")
        assert func is first
