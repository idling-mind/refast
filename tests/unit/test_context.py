"""Tests for Context class and Callback."""

import pytest
from refast.context import Context, Callback
from refast import RefastApp


class TestCallback:
    """Tests for Callback dataclass."""
    
    def test_callback_has_id(self):
        """Test Callback stores an ID."""
        def my_func():
            pass
        
        cb = Callback(id="test-id", func=my_func)
        assert cb.id == "test-id"
    
    def test_callback_has_func(self):
        """Test Callback stores a function."""
        def my_func():
            pass
        
        cb = Callback(id="test-id", func=my_func)
        assert cb.func == my_func
    
    def test_callback_default_bound_args(self):
        """Test Callback has empty bound_args by default."""
        def my_func():
            pass
        
        cb = Callback(id="test-id", func=my_func)
        assert cb.bound_args == {}
    
    def test_callback_with_bound_args(self):
        """Test Callback stores bound arguments."""
        def my_func():
            pass
        
        cb = Callback(id="test-id", func=my_func, bound_args={"x": 1, "y": 2})
        assert cb.bound_args == {"x": 1, "y": 2}
    
    def test_callback_serialize(self):
        """Test Callback serialization."""
        def my_func():
            pass
        
        cb = Callback(id="test-id", func=my_func, bound_args={"x": 1})
        serialized = cb.serialize()
        
        assert serialized["callbackId"] == "test-id"
        assert serialized["boundArgs"] == {"x": 1}
    
    def test_callback_serialize_empty_args(self):
        """Test Callback serialization with empty args."""
        def my_func():
            pass
        
        cb = Callback(id="test-id", func=my_func)
        serialized = cb.serialize()
        
        assert serialized["callbackId"] == "test-id"
        assert serialized["boundArgs"] == {}


class TestContext:
    """Tests for Context class."""
    
    def test_context_creation(self):
        """Test Context can be created."""
        ctx = Context()
        assert ctx is not None
    
    def test_state_is_dict(self):
        """Test state property returns a dict."""
        ctx = Context()
        assert isinstance(ctx.state, dict)
    
    def test_state_is_mutable(self):
        """Test state can be modified."""
        ctx = Context()
        ctx.state["count"] = 0
        ctx.state["count"] += 1
        assert ctx.state["count"] == 1
    
    def test_session_property(self):
        """Test session property returns a Session."""
        ctx = Context()
        session = ctx.session
        assert session is not None
    
    def test_session_is_cached(self):
        """Test session is created once and cached."""
        ctx = Context()
        session1 = ctx.session
        session2 = ctx.session
        assert session1 is session2


class TestContextCallback:
    """Tests for Context.callback() method."""
    
    def test_callback_creates_callback_object(self):
        """Test callback method creates a Callback."""
        ctx = Context()
        
        def my_handler():
            pass
        
        cb = ctx.callback(my_handler)
        assert isinstance(cb, Callback)
    
    def test_callback_with_bound_args(self):
        """Test callback with bound arguments."""
        ctx = Context()
        
        def my_handler():
            pass
        
        cb = ctx.callback(my_handler, item_id=123, name="test")
        assert cb.bound_args == {"item_id": 123, "name": "test"}
    
    def test_callback_generates_unique_ids(self):
        """Test each callback gets a unique ID."""
        ctx = Context()
        
        def handler():
            pass
        
        cb1 = ctx.callback(handler)
        cb2 = ctx.callback(handler)
        cb3 = ctx.callback(handler)
        
        assert cb1.id != cb2.id
        assert cb2.id != cb3.id
        assert cb1.id != cb3.id
    
    def test_callback_registers_with_app(self):
        """Test callback is registered with app."""
        app = RefastApp()
        ctx = Context(app=app)
        
        def my_handler():
            pass
        
        cb = ctx.callback(my_handler)
        
        assert app.get_callback(cb.id) == my_handler


class TestContextWithoutWebSocket:
    """Tests for Context methods without WebSocket."""
    
    @pytest.mark.asyncio
    async def test_push_update_without_websocket(self):
        """Test push_update does nothing without websocket."""
        ctx = Context()
        ctx.state["count"] = 1
        # Should not raise
        await ctx.push_update()
    
    @pytest.mark.asyncio
    async def test_replace_without_websocket(self):
        """Test replace does nothing without websocket."""
        ctx = Context()
        # Should not raise
        await ctx.replace("target-id", {"type": "Text"})
    
    @pytest.mark.asyncio
    async def test_append_without_websocket(self):
        """Test append does nothing without websocket."""
        ctx = Context()
        await ctx.append("target-id", {"type": "Text"})
    
    @pytest.mark.asyncio
    async def test_prepend_without_websocket(self):
        """Test prepend does nothing without websocket."""
        ctx = Context()
        await ctx.prepend("target-id", {"type": "Text"})
    
    @pytest.mark.asyncio
    async def test_remove_without_websocket(self):
        """Test remove does nothing without websocket."""
        ctx = Context()
        await ctx.remove("target-id")
    
    @pytest.mark.asyncio
    async def test_update_props_without_websocket(self):
        """Test update_props does nothing without websocket."""
        ctx = Context()
        await ctx.update_props("target-id", {"label": "New"})
    
    @pytest.mark.asyncio
    async def test_navigate_without_websocket(self):
        """Test navigate does nothing without websocket."""
        ctx = Context()
        await ctx.navigate("/new-page")
    
    @pytest.mark.asyncio
    async def test_show_toast_without_websocket(self):
        """Test show_toast does nothing without websocket."""
        ctx = Context()
        await ctx.show_toast("Hello!")
    
    @pytest.mark.asyncio
    async def test_push_event_without_websocket(self):
        """Test push_event does nothing without websocket."""
        ctx = Context()
        await ctx.push_event("custom:event", {"data": "value"})
    
    @pytest.mark.asyncio
    async def test_broadcast_without_websocket(self):
        """Test broadcast does nothing without websocket."""
        ctx = Context()
        await ctx.broadcast("custom:event", {"data": "value"})
