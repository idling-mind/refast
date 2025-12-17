"""Tests for EventManager."""

import pytest
from refast.events.manager import EventManager
from refast.events.types import Event


class TestEventManagerRegistration:
    """Tests for event handler registration."""

    def test_register_handler_with_decorator(self):
        """Test registering handler with decorator."""
        manager = EventManager()

        @manager.on("test:event")
        async def handler(ctx, event):
            pass

        assert len(manager.get_handlers("test:event")) == 1

    def test_register_handler_programmatically(self):
        """Test registering handler programmatically."""
        manager = EventManager()

        async def handler(ctx, event):
            pass

        manager.register_handler("test:event", handler)
        assert len(manager.get_handlers("test:event")) == 1

    def test_unregister_handler(self):
        """Test unregistering a handler."""
        manager = EventManager()

        async def handler(ctx, event):
            pass

        manager.register_handler("test:event", handler)
        assert len(manager.get_handlers("test:event")) == 1

        manager.unregister_handler("test:event", handler)
        assert len(manager.get_handlers("test:event")) == 0

    def test_multiple_handlers(self):
        """Test multiple handlers for same event."""
        manager = EventManager()

        @manager.on("test:event")
        async def handler1(ctx, event):
            pass

        @manager.on("test:event")
        async def handler2(ctx, event):
            pass

        assert len(manager.get_handlers("test:event")) == 2

    def test_get_handlers_empty(self):
        """Test getting handlers for unknown event."""
        manager = EventManager()
        assert manager.get_handlers("unknown") == []


class TestEventManagerEmit:
    """Tests for event emission."""

    @pytest.mark.asyncio
    async def test_emit_to_handler(self):
        """Test emitting event to handler."""
        manager = EventManager()
        results = []

        @manager.on("test:event")
        async def handler(ctx, event):
            results.append(event.data)

        await manager.emit("test:event", {"value": 42})
        assert len(results) == 1
        assert results[0]["value"] == 42

    @pytest.mark.asyncio
    async def test_emit_to_multiple_handlers(self):
        """Test emitting to multiple handlers."""
        manager = EventManager()
        results = []

        @manager.on("test:event")
        async def handler1(ctx, event):
            results.append("handler1")

        @manager.on("test:event")
        async def handler2(ctx, event):
            results.append("handler2")

        await manager.emit("test:event", {})
        assert results == ["handler1", "handler2"]

    @pytest.mark.asyncio
    async def test_emit_no_handlers(self):
        """Test emitting when no handlers registered."""
        manager = EventManager()
        results = await manager.emit("unknown:event", {})
        assert results == []

    @pytest.mark.asyncio
    async def test_emit_returns_results(self):
        """Test emit returns handler results."""
        manager = EventManager()

        @manager.on("test:event")
        async def handler(ctx, event):
            return event.data["value"] * 2

        results = await manager.emit("test:event", {"value": 21})
        assert results == [42]

    @pytest.mark.asyncio
    async def test_emit_with_context(self):
        """Test emit passes context to handlers."""
        manager = EventManager()
        received_ctx = []

        @manager.on("test:event")
        async def handler(ctx, event):
            received_ctx.append(ctx)

        ctx_value = "test_context"
        await manager.emit("test:event", {}, ctx=ctx_value)
        assert received_ctx[0] == ctx_value


class TestEventManagerCallbacks:
    """Tests for callback management."""

    def test_register_callback(self):
        """Test registering a callback."""
        manager = EventManager()

        def my_callback(ctx):
            pass

        manager.register_callback("cb-1", my_callback)
        assert manager.get_callback("cb-1") == my_callback

    def test_get_callback_not_found(self):
        """Test getting unknown callback."""
        manager = EventManager()
        assert manager.get_callback("unknown") is None

    @pytest.mark.asyncio
    async def test_invoke_async_callback(self):
        """Test invoking async callback."""
        manager = EventManager()

        async def my_callback(ctx, item_id: int):
            return item_id * 2

        manager.register_callback("cb-1", my_callback)

        result = await manager.invoke_callback(
            "cb-1",
            ctx=None,
            event_data={"boundArgs": {"item_id": 21}},
        )
        assert result == 42

    @pytest.mark.asyncio
    async def test_invoke_sync_callback(self):
        """Test invoking sync callback."""
        manager = EventManager()

        def my_callback(ctx, value: int):
            return value + 10

        manager.register_callback("cb-1", my_callback)

        result = await manager.invoke_callback(
            "cb-1",
            ctx=None,
            event_data={"boundArgs": {"value": 32}},
        )
        assert result == 42

    @pytest.mark.asyncio
    async def test_invoke_callback_with_merged_args(self):
        """Test callback with merged bound and call args."""
        manager = EventManager()

        async def my_callback(ctx, a: int, b: int):
            return a + b

        manager.register_callback("cb-1", my_callback)

        result = await manager.invoke_callback(
            "cb-1",
            ctx=None,
            event_data={
                "boundArgs": {"a": 20},
                "data": {"b": 22},
            },
        )
        assert result == 42

    @pytest.mark.asyncio
    async def test_invoke_callback_not_found(self):
        """Test invoking unknown callback."""
        manager = EventManager()

        result = await manager.invoke_callback(
            "unknown",
            ctx=None,
            event_data={},
        )
        assert result is None


class TestEventManagerMiddleware:
    """Tests for middleware."""

    @pytest.mark.asyncio
    async def test_middleware_runs(self):
        """Test middleware is called."""
        manager = EventManager()
        order = []

        async def middleware(ctx, event, next):
            order.append("middleware-before")
            result = await next(ctx, event)
            order.append("middleware-after")
            return result

        manager.add_middleware(middleware)

        @manager.on("test")
        async def handler(ctx, event):
            order.append("handler")

        await manager.emit("test", {})
        assert order == ["middleware-before", "handler", "middleware-after"]

    @pytest.mark.asyncio
    async def test_multiple_middleware(self):
        """Test multiple middleware in order."""
        manager = EventManager()
        order = []

        async def middleware1(ctx, event, next):
            order.append("m1-before")
            result = await next(ctx, event)
            order.append("m1-after")
            return result

        async def middleware2(ctx, event, next):
            order.append("m2-before")
            result = await next(ctx, event)
            order.append("m2-after")
            return result

        manager.add_middleware(middleware1)
        manager.add_middleware(middleware2)

        @manager.on("test")
        async def handler(ctx, event):
            order.append("handler")

        await manager.emit("test", {})
        assert order == [
            "m1-before",
            "m2-before",
            "handler",
            "m2-after",
            "m1-after",
        ]

    @pytest.mark.asyncio
    async def test_middleware_can_modify_event(self):
        """Test middleware can modify event."""
        manager = EventManager()

        async def add_data_middleware(ctx, event, next):
            event.data["added"] = "by_middleware"
            return await next(ctx, event)

        manager.add_middleware(add_data_middleware)

        received_data = []

        @manager.on("test")
        async def handler(ctx, event):
            received_data.append(event.data)

        await manager.emit("test", {"original": True})
        assert received_data[0]["original"] is True
        assert received_data[0]["added"] == "by_middleware"

    @pytest.mark.asyncio
    async def test_no_middleware(self):
        """Test handler runs without middleware."""
        manager = EventManager()
        called = []

        @manager.on("test")
        async def handler(ctx, event):
            called.append(True)

        await manager.emit("test", {})
        assert called == [True]
