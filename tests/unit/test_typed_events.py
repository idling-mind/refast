"""Tests for typed event handlers and callbacks."""

import pytest
from pydantic import BaseModel, ValidationError

from refast.app import RefastApp
from refast.events.types import Event
from refast.router import _filter_callback_kwargs


class UserLoginPayload(BaseModel):
    user_id: int
    session_token: str


class SearchPayload(BaseModel):
    query: str
    limit: int = 10


class TestTypedEvents:
    """Tests for strongly typed events using Pydantic."""

    @pytest.mark.asyncio
    async def test_typed_event_handler_success(self):
        """Test event handler with typed Event payload resolves correctly."""
        app = RefastApp()
        received_event = None

        @app.on("user:login")
        async def handle_login(ctx, event: Event[UserLoginPayload]):
            nonlocal received_event
            received_event = event

        # Emit event with valid dict payload
        await app.events.emit(
            "user:login",
            {"user_id": 123, "session_token": "secret_token"},
        )

        assert received_event is not None
        assert isinstance(received_event.data, UserLoginPayload)
        assert received_event.data.user_id == 123
        assert received_event.data.session_token == "secret_token"

    @pytest.mark.asyncio
    async def test_typed_event_handler_validation_error(self):
        """Test event handler raises ValidationError when input payload is invalid."""
        app = RefastApp()

        @app.on("user:login")
        async def handle_login(ctx, event: Event[UserLoginPayload]):
            pass

        # Emit event with missing fields (should raise ValidationError)
        with pytest.raises(ValidationError) as exc_info:
            await app.events.emit("user:login", {"user_id": 123})

        assert "session_token" in str(exc_info.value)

    def test_typed_callback_kwargs_success(self):
        """Test callback parameter validation with valid dictionary."""

        async def callback(ctx, payload: SearchPayload):
            pass

        event_data = {"query": "refast", "limit": 5}
        callback_data = {}

        kwargs = _filter_callback_kwargs(callback, event_data, callback_data)

        assert "payload" in kwargs
        assert isinstance(kwargs["payload"], SearchPayload)
        assert kwargs["payload"].query == "refast"
        assert kwargs["payload"].limit == 5

    def test_typed_callback_kwargs_defaults(self):
        """Test callback parameter validation uses model defaults."""

        async def callback(ctx, payload: SearchPayload):
            pass

        event_data = {"query": "refast"}
        callback_data = {}

        kwargs = _filter_callback_kwargs(callback, event_data, callback_data)

        assert "payload" in kwargs
        assert isinstance(kwargs["payload"], SearchPayload)
        assert kwargs["payload"].query == "refast"
        assert kwargs["payload"].limit == 10  # default value

    def test_typed_callback_kwargs_invalid(self):
        """Test callback parameter validation raises ValidationError for invalid input."""

        async def callback(ctx, payload: SearchPayload):
            pass

        # query is missing
        event_data = {"limit": 5}
        callback_data = {}

        with pytest.raises(ValidationError):
            _filter_callback_kwargs(callback, event_data, callback_data)

    def test_app_event_handlers_compat_property(self):
        """Test RefastApp._event_handlers backward compatibility property."""
        app = RefastApp()

        @app.on_event("test:compat")
        async def handler(ctx, event):
            pass

        assert "test:compat" in app._event_handlers
        assert app._event_handlers["test:compat"] == handler

    def test_websocket_callback_validation_error(self):
        """Test that validation error in callback over WebSocket returns a structured toast notification."""
        from fastapi import FastAPI
        from fastapi.testclient import TestClient
        from refast.components import Button
        from refast.context import Context

        ui = RefastApp()

        async def search_callback(ctx: Context, payload: SearchPayload):
            pass

        @ui.page("/")
        def home(ctx: Context):
            return Button("Search", on_click=ctx.callback(search_callback))

        app = FastAPI()
        app.include_router(ui.router)
        client = TestClient(app)

        # Connect and get page html (to set up context session/callbacks)
        resp = client.get("/")
        assert resp.status_code == 200

        with client.websocket_connect("/ws") as ws:
            # First send store_init to initialize the page session & callbacks
            ws.send_json(
                {
                    "type": "store_init",
                    "data": {},
                    "path": "/",
                }
            )
            # Read store_ready and page_render response
            ws.receive_json() # page_render
            ws.receive_json() # store_ready

            # Retrieve registered callback ID from Context
            contexts = ui._router.active_contexts
            assert len(contexts) == 1
            ctx = contexts[0]
            callback_id = list(ctx._callbacks.keys())[0]

            # Send callback trigger message with INVALID data (missing 'query')
            ws.send_json(
                {
                    "type": "callback",
                    "callbackId": callback_id,
                    "data": {},
                    "eventData": {"limit": 5},
                }
            )

            # Receive the response — should be a toast message reporting the validation error
            response = ws.receive_json()
            assert response["type"] == "toast"
            assert "Validation Error" in response["message"]
            assert "query" in response["description"]
            assert "Field required" in response["description"]

    @pytest.mark.asyncio
    async def test_custom_callback_on_error_handler(self):
        """Test that custom callback error handler is invoked with (ctx, exc, **combined) when validation fails."""
        from fastapi import FastAPI
        from fastapi.testclient import TestClient
        from refast.components import Button
        from refast.context import Context

        ui = RefastApp()
        error_called_with = None

        async def error_handler(ctx: Context, error: Exception, **kwargs):
            nonlocal error_called_with
            error_called_with = (error, kwargs)
            ctx.state["query_result"] = "Error handled!"
            await ctx.show_toast("Error Handled Customly", variant="success")

        async def search_callback(ctx: Context, payload: SearchPayload):
            pass

        @ui.page("/")
        def home(ctx: Context):
            return Button("Search", on_click=ctx.callback(search_callback, on_error=error_handler))

        app = FastAPI()
        app.include_router(ui.router)
        client = TestClient(app)

        resp = client.get("/")
        assert resp.status_code == 200

        with client.websocket_connect("/ws") as ws:
            ws.send_json({"type": "store_init", "data": {}, "path": "/"})
            ws.receive_json() # page_render
            ws.receive_json() # store_ready

            contexts = ui._router.active_contexts
            assert len(contexts) == 1
            ctx = contexts[0]
            callback_id = list(ctx._callbacks.keys())[0]

            # Trigger callback with invalid data (missing query)
            ws.send_json(
                {
                    "type": "callback",
                    "callbackId": callback_id,
                    "data": {"custom_arg": "value"},
                    "eventData": {"limit": 5},
                }
            )

            # Receive the custom success toast from the error handler (instead of default validation error)
            response = ws.receive_json()
            assert response["type"] == "toast"
            assert response["message"] == "Error Handled Customly"

            # Check that state was updated
            assert ctx.state["query_result"] == "Error handled!"
            assert error_called_with is not None
            assert isinstance(error_called_with[0], ValidationError)
            # kwargs should have raw merged eventData and callback data
            assert error_called_with[1] == {"limit": 5, "custom_arg": "value"}

    @pytest.mark.asyncio
    async def test_custom_event_on_error_handler(self):
        """Test that custom event error handler is invoked with (ctx, exc, event) when validation fails."""
        from refast.context import Context

        ui = RefastApp()
        error_called_with = None

        async def error_handler(ctx: Context, error: Exception, **kwargs):
            nonlocal error_called_with
            error_called_with = (error, kwargs)

        @ui.on("search:query_event", on_error=error_handler)
        async def handle_search_event(ctx: Context, event: Event[SearchPayload]):
            pass

        # Emit invalid payload
        invalid_data = {"limit": 5}
        # Since emit runs on the server directly, we check that emit invokes the error handler
        # and doesn't propagate ValidationError
        await ui.events.emit("search:query_event", invalid_data, ctx=None)

        assert error_called_with is not None
        assert isinstance(error_called_with[0], ValidationError)
        assert "event" in error_called_with[1]
        assert error_called_with[1]["event"].data == invalid_data


