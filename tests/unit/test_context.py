"""Tests for Context class and Callback."""

import pytest

from refast import RefastApp
from refast.context import BoundJsCallback, Callback, Context, JsAction, JsCallback


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

    def test_state_is_state_object(self):
        """Test state property returns a State object."""
        ctx = Context()
        from refast.state import State

        assert isinstance(ctx.state, State)

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
    async def test_update_text_without_websocket(self):
        """Test update_text does nothing without websocket."""
        ctx = Context()
        await ctx.update_text("target-id", "New text")

    @pytest.mark.asyncio
    async def test_refresh_without_websocket(self):
        """Test refresh does nothing without websocket."""
        ctx = Context()
        await ctx.refresh("/")

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
        """Test broadcast returns 0 without app."""
        ctx = Context()
        result = await ctx.broadcast("custom:event", {"data": "value"})
        assert result == 0


class TestJsCallback:
    """Tests for JsCallback dataclass."""

    def test_js_callback_has_code(self):
        """Test JsCallback stores JavaScript code."""
        cb = JsCallback(code="alert('Hello!')")
        assert cb.code == "alert('Hello!')"

    def test_js_callback_default_bound_args(self):
        """Test JsCallback has empty bound_args by default."""
        cb = JsCallback(code="console.log(1)")
        assert cb.bound_args == {}

    def test_js_callback_with_bound_args(self):
        """Test JsCallback stores bound arguments."""
        cb = JsCallback(code="deleteItem(args.id)", bound_args={"id": 123})
        assert cb.bound_args == {"id": 123}

    def test_js_callback_serialize(self):
        """Test JsCallback serialization."""
        cb = JsCallback(code="alert(args.msg)", bound_args={"msg": "Hello"})
        serialized = cb.serialize()

        assert serialized["jsFunction"] == "alert(args.msg)"
        assert serialized["boundArgs"] == {"msg": "Hello"}

    def test_js_callback_serialize_empty_args(self):
        """Test JsCallback serialization with empty args."""
        cb = JsCallback(code="console.log('test')")
        serialized = cb.serialize()

        assert serialized["jsFunction"] == "console.log('test')"
        assert serialized["boundArgs"] == {}

    def test_js_callback_no_callback_id(self):
        """Test JsCallback does not have a callbackId."""
        cb = JsCallback(code="test()")
        serialized = cb.serialize()
        
        assert "callbackId" not in serialized
        assert "jsFunction" in serialized


class TestJsAction:
    """Tests for JsAction dataclass."""

    def test_js_action_has_code(self):
        """Test JsAction stores JavaScript code."""
        action = JsAction(code="window.scrollTo(0, 0)")
        assert action.code == "window.scrollTo(0, 0)"

    def test_js_action_default_args(self):
        """Test JsAction has empty args by default."""
        action = JsAction(code="test()")
        assert action.args == {}

    def test_js_action_with_args(self):
        """Test JsAction stores arguments."""
        action = JsAction(code="focus(args.id)", args={"id": "input-1"})
        assert action.args == {"id": "input-1"}


class TestContextJs:
    """Tests for Context.js() method."""

    def test_js_creates_js_callback_object(self):
        """Test js method creates a JsCallback."""
        ctx = Context()
        cb = ctx.js("alert('Hello!')")
        assert isinstance(cb, JsCallback)

    def test_js_stores_code(self):
        """Test js method stores the JavaScript code."""
        ctx = Context()
        cb = ctx.js("console.log('test')")
        assert cb.code == "console.log('test')"

    def test_js_with_bound_args(self):
        """Test js with bound arguments."""
        ctx = Context()
        cb = ctx.js("deleteItem(args.item_id)", item_id=123, name="test")
        assert cb.bound_args == {"item_id": 123, "name": "test"}

    def test_js_serialize_format(self):
        """Test js callback serializes correctly."""
        ctx = Context()
        cb = ctx.js("window.myFunc(args.data)", data={"key": "value"})
        serialized = cb.serialize()

        assert "jsFunction" in serialized
        assert serialized["jsFunction"] == "window.myFunc(args.data)"
        assert serialized["boundArgs"] == {"data": {"key": "value"}}

    def test_js_does_not_register_with_app(self):
        """Test js callback is not registered with app (it's client-side)."""
        app = RefastApp()
        ctx = Context(app=app)
        cb = ctx.js("alert('test')")

        # JsCallbacks don't have an id to register
        assert not hasattr(cb, "id") or cb.code == "alert('test')"


class TestContextCallJsWithoutWebSocket:
    """Tests for Context.call_js() method without WebSocket."""

    @pytest.mark.asyncio
    async def test_call_js_without_websocket(self):
        """Test call_js does nothing without websocket."""
        ctx = Context()
        # Should not raise
        await ctx.call_js("console.log('test')")

    @pytest.mark.asyncio
    async def test_call_js_with_args_without_websocket(self):
        """Test call_js with args does nothing without websocket."""
        ctx = Context()
        # Should not raise
        await ctx.call_js("focus(args.id)", id="input-1")


class TestBoundJsCallback:
    """Tests for BoundJsCallback dataclass."""

    def test_bound_js_callback_has_target_id(self):
        """Test BoundJsCallback stores a target ID."""
        cb = BoundJsCallback(target_id="my-canvas", method_name="clearCanvas")
        assert cb.target_id == "my-canvas"

    def test_bound_js_callback_has_method_name(self):
        """Test BoundJsCallback stores a method name."""
        cb = BoundJsCallback(target_id="my-canvas", method_name="clearCanvas")
        assert cb.method_name == "clearCanvas"

    def test_bound_js_callback_default_args(self):
        """Test BoundJsCallback has empty args by default."""
        cb = BoundJsCallback(target_id="my-canvas", method_name="clearCanvas")
        assert cb.args == {}

    def test_bound_js_callback_with_args(self):
        """Test BoundJsCallback stores arguments."""
        cb = BoundJsCallback(
            target_id="my-canvas", method_name="eraseMode", args={"erase": True}
        )
        assert cb.args == {"erase": True}

    def test_bound_js_callback_serialize(self):
        """Test BoundJsCallback serialization."""
        cb = BoundJsCallback(
            target_id="my-canvas", method_name="loadPaths", args={"paths": [1, 2, 3]}
        )
        serialized = cb.serialize()

        assert "boundMethod" in serialized
        assert serialized["boundMethod"]["targetId"] == "my-canvas"
        assert serialized["boundMethod"]["methodName"] == "loadPaths"
        assert serialized["boundMethod"]["args"] == {"paths": [1, 2, 3]}

    def test_bound_js_callback_serialize_empty_args(self):
        """Test BoundJsCallback serialization with empty args."""
        cb = BoundJsCallback(target_id="my-canvas", method_name="undo")
        serialized = cb.serialize()

        assert serialized["boundMethod"]["targetId"] == "my-canvas"
        assert serialized["boundMethod"]["methodName"] == "undo"
        assert serialized["boundMethod"]["args"] == {}


class TestContextBoundJs:
    """Tests for Context.bound_js() method."""

    def test_bound_js_creates_bound_js_callback_object(self):
        """Test bound_js method creates a BoundJsCallback."""
        ctx = Context()
        cb = ctx.bound_js("my-canvas", "clearCanvas")
        assert isinstance(cb, BoundJsCallback)

    def test_bound_js_stores_target_id(self):
        """Test bound_js method stores the target ID."""
        ctx = Context()
        cb = ctx.bound_js("my-canvas", "clearCanvas")
        assert cb.target_id == "my-canvas"

    def test_bound_js_stores_method_name(self):
        """Test bound_js method stores the method name."""
        ctx = Context()
        cb = ctx.bound_js("my-canvas", "undo")
        assert cb.method_name == "undo"

    def test_bound_js_with_args(self):
        """Test bound_js with arguments."""
        ctx = Context()
        cb = ctx.bound_js("my-canvas", "eraseMode", erase=True)
        assert cb.args == {"erase": True}

    def test_bound_js_with_multiple_args(self):
        """Test bound_js with multiple arguments."""
        ctx = Context()
        cb = ctx.bound_js("my-canvas", "loadPaths", paths=[1, 2], append=False)
        assert cb.args == {"paths": [1, 2], "append": False}

    def test_bound_js_serialize_format(self):
        """Test bound_js callback serializes correctly."""
        ctx = Context()
        cb = ctx.bound_js("my-canvas", "exportImage", image_type="png")
        serialized = cb.serialize()

        assert "boundMethod" in serialized
        assert serialized["boundMethod"]["targetId"] == "my-canvas"
        assert serialized["boundMethod"]["methodName"] == "exportImage"
        assert serialized["boundMethod"]["args"] == {"image_type": "png"}

    def test_bound_js_does_not_register_with_app(self):
        """Test bound_js callback is not registered with app (it's client-side)."""
        app = RefastApp()
        ctx = Context(app=app)
        cb = ctx.bound_js("my-canvas", "clearCanvas")

        # BoundJsCallbacks don't have a callback id to register
        assert cb.target_id == "my-canvas"


class TestContextCallBoundJsWithoutWebSocket:
    """Tests for Context.call_bound_js() method without WebSocket."""

    @pytest.mark.asyncio
    async def test_call_bound_js_without_websocket(self):
        """Test call_bound_js does nothing without websocket."""
        ctx = Context()
        # Should not raise
        await ctx.call_bound_js("my-canvas", "clearCanvas")

    @pytest.mark.asyncio
    async def test_call_bound_js_with_args_without_websocket(self):
        """Test call_bound_js with args does nothing without websocket."""
        ctx = Context()
        # Should not raise
        await ctx.call_bound_js("my-canvas", "eraseMode", erase=True)

    @pytest.mark.asyncio
    async def test_call_bound_js_with_multiple_args_without_websocket(self):
        """Test call_bound_js with multiple args does nothing without websocket."""
        ctx = Context()
        # Should not raise
        await ctx.call_bound_js("my-canvas", "loadPaths", paths=[1, 2, 3], clear=True)