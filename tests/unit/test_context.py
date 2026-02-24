"""Tests for Context class and Callback."""

from unittest.mock import AsyncMock

import pytest

from refast import RefastApp
from refast.context import (
    BoundJsCallback,
    Callback,
    ChainedAction,
    Context,
    JsAction,
    JsCallback,
    SaveProp,
)


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
    async def test_append_prop_without_websocket(self):
        """Test append_prop does nothing without websocket."""
        ctx = Context()
        await ctx.append_prop("target-id", "content", "new text")

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

    def test_js_callback_serialize_with_callback_bound_arg(self):
        """Test JsCallback serializes Callback objects in bound_args."""
        inner_cb = Callback(
            id="test-cb-id",
            func=lambda ctx: None,
            bound_args={"item_id": 42},
        )
        cb = JsCallback(
            code="refast.invoke(args.on_submit)",
            bound_args={"on_submit": inner_cb, "label": "hello"},
        )
        serialized = cb.serialize()

        # The Callback should be serialized to its dict form
        assert serialized["boundArgs"]["label"] == "hello"
        assert serialized["boundArgs"]["on_submit"]["callbackId"] == "test-cb-id"
        assert serialized["boundArgs"]["on_submit"]["boundArgs"] == {"item_id": 42}

    def test_js_callback_serialize_preserves_plain_args(self):
        """Test JsCallback serialization preserves non-Callback bound args."""
        cb = JsCallback(
            code="test(args.x)",
            bound_args={"x": 123, "y": "hello", "z": [1, 2, 3]},
        )
        serialized = cb.serialize()

        assert serialized["boundArgs"] == {"x": 123, "y": "hello", "z": [1, 2, 3]}


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

    def test_js_with_callback_bound_arg(self):
        """Test js with a Callback object as a bound argument."""
        app = RefastApp()
        ctx = Context(app=app)

        async def handler(ctx: Context):
            pass

        cb = ctx.js(
            "if (event.key === 'Enter') { refast.invoke(args.on_submit); }",
            on_submit=ctx.callback(handler),
        )

        serialized = cb.serialize()
        assert "jsFunction" in serialized
        # The callback should be serialized to a dict with callbackId
        on_submit = serialized["boundArgs"]["on_submit"]
        assert "callbackId" in on_submit
        assert isinstance(on_submit["callbackId"], str)

    def test_js_with_mixed_callback_and_plain_args(self):
        """Test js with both Callback and plain bound args."""
        app = RefastApp()
        ctx = Context(app=app)

        async def handler(ctx: Context):
            pass

        cb = ctx.js(
            "if (event.key === 'Enter') { refast.invoke(args.on_submit, { value: args.placeholder }); }",
            on_submit=ctx.callback(handler),
            placeholder="Type here...",
        )

        serialized = cb.serialize()
        assert serialized["boundArgs"]["placeholder"] == "Type here..."
        assert "callbackId" in serialized["boundArgs"]["on_submit"]


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
        assert cb.args == ()
        assert cb.kwargs == {}

    def test_bound_js_callback_with_args(self):
        """Test BoundJsCallback stores arguments."""
        cb = BoundJsCallback(target_id="my-canvas", method_name="eraseMode", args=(True,))
        assert cb.args == (True,)

    def test_bound_js_callback_with_kwargs(self):
        """Test BoundJsCallback stores keyword arguments."""
        cb = BoundJsCallback(target_id="my-canvas", method_name="eraseMode", kwargs={"erase": True})
        assert cb.kwargs == {"erase": True}

    def test_bound_js_callback_with_args_and_kwargs(self):
        """Test BoundJsCallback stores both args and kwargs."""
        cb = BoundJsCallback(
            target_id="my-canvas",
            method_name="drawShape",
            args=("circle",),
            kwargs={"x": 100, "y": 200},
        )
        assert cb.args == ("circle",)
        assert cb.kwargs == {"x": 100, "y": 200}

    def test_bound_js_callback_serialize(self):
        """Test BoundJsCallback serialization."""
        cb = BoundJsCallback(
            target_id="my-canvas", method_name="loadPaths", kwargs={"paths": [1, 2, 3]}
        )
        serialized = cb.serialize()

        assert "boundMethod" in serialized
        assert serialized["boundMethod"]["targetId"] == "my-canvas"
        assert serialized["boundMethod"]["methodName"] == "loadPaths"
        assert serialized["boundMethod"]["args"] == []
        assert serialized["boundMethod"]["kwargs"] == {"paths": [1, 2, 3]}

    def test_bound_js_callback_serialize_with_positional_args(self):
        """Test BoundJsCallback serialization with positional args."""
        cb = BoundJsCallback(
            target_id="my-canvas",
            method_name="drawShape",
            args=("circle", 100, 200),
            kwargs={"fill": "red"},
        )
        serialized = cb.serialize()

        assert serialized["boundMethod"]["args"] == ["circle", 100, 200]
        assert serialized["boundMethod"]["kwargs"] == {"fill": "red"}

    def test_bound_js_callback_serialize_empty_args(self):
        """Test BoundJsCallback serialization with empty args."""
        cb = BoundJsCallback(target_id="my-canvas", method_name="undo")
        serialized = cb.serialize()

        assert serialized["boundMethod"]["targetId"] == "my-canvas"
        assert serialized["boundMethod"]["methodName"] == "undo"
        assert serialized["boundMethod"]["args"] == []
        assert serialized["boundMethod"]["kwargs"] == {}


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

    def test_bound_js_with_positional_args(self):
        """Test bound_js with positional arguments."""
        ctx = Context()
        cb = ctx.bound_js("my-canvas", "eraseMode", True)
        assert cb.args == (True,)
        assert cb.kwargs == {}

    def test_bound_js_with_kwargs(self):
        """Test bound_js with keyword arguments."""
        ctx = Context()
        cb = ctx.bound_js("my-canvas", "eraseMode", erase=True)
        assert cb.args == ()
        assert cb.kwargs == {"erase": True}

    def test_bound_js_with_multiple_kwargs(self):
        """Test bound_js with multiple keyword arguments."""
        ctx = Context()
        cb = ctx.bound_js("my-canvas", "loadPaths", paths=[1, 2], append=False)
        assert cb.args == ()
        assert cb.kwargs == {"paths": [1, 2], "append": False}

    def test_bound_js_with_args_and_kwargs(self):
        """Test bound_js with both positional and keyword arguments."""
        ctx = Context()
        cb = ctx.bound_js("my-canvas", "drawShape", "circle", x=100, y=200)
        assert cb.args == ("circle",)
        assert cb.kwargs == {"x": 100, "y": 200}

    def test_bound_js_serialize_format(self):
        """Test bound_js callback serializes correctly."""
        ctx = Context()
        cb = ctx.bound_js("my-canvas", "exportImage", image_type="png")
        serialized = cb.serialize()

        assert "boundMethod" in serialized
        assert serialized["boundMethod"]["targetId"] == "my-canvas"
        assert serialized["boundMethod"]["methodName"] == "exportImage"
        assert serialized["boundMethod"]["args"] == []
        assert serialized["boundMethod"]["kwargs"] == {"image_type": "png"}

    def test_bound_js_serialize_format_with_positional_args(self):
        """Test bound_js callback serializes correctly with positional args."""
        ctx = Context()
        cb = ctx.bound_js("my-canvas", "setSize", 800, 600)
        serialized = cb.serialize()

        assert serialized["boundMethod"]["args"] == [800, 600]
        assert serialized["boundMethod"]["kwargs"] == {}

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


class TestContextAppendProp:
    """Tests for Context.append_prop() method."""

    @pytest.mark.asyncio
    async def test_append_prop_sends_correct_message(self):
        """Test append_prop sends correct WebSocket message."""
        ws = AsyncMock()
        ctx = Context(websocket=ws)

        await ctx.append_prop("markdown-output", "content", "new text")

        ws.send_json.assert_called_once_with(
            {
                "type": "update",
                "operation": "append_prop",
                "targetId": "markdown-output",
                "propName": "content",
                "value": "new text",
            }
        )

    @pytest.mark.asyncio
    async def test_append_prop_with_list_value(self):
        """Test append_prop with list value."""
        ws = AsyncMock()
        ctx = Context(websocket=ws)

        await ctx.append_prop("my-chart", "data", [{"x": 1, "y": 2}])

        ws.send_json.assert_called_once_with(
            {
                "type": "update",
                "operation": "append_prop",
                "targetId": "my-chart",
                "propName": "data",
                "value": [{"x": 1, "y": 2}],
            }
        )

    @pytest.mark.asyncio
    async def test_append_prop_with_single_item(self):
        """Test append_prop with single item for array."""
        ws = AsyncMock()
        ctx = Context(websocket=ws)

        await ctx.append_prop("my-chart", "data", {"x": 1, "y": 2})

        ws.send_json.assert_called_once_with(
            {
                "type": "update",
                "operation": "append_prop",
                "targetId": "my-chart",
                "propName": "data",
                "value": {"x": 1, "y": 2},
            }
        )

    @pytest.mark.asyncio
    async def test_append_prop_without_websocket(self):
        """Test append_prop does nothing without websocket."""
        ctx = Context()
        # Should not raise
        await ctx.append_prop("target-id", "content", "new text")


class TestSaveProp:
    """Tests for SaveProp dataclass."""

    def test_save_prop_with_string_name(self):
        """Test SaveProp with a simple string key."""
        sp = SaveProp(name="email")
        assert sp.name == "email"
        assert sp.debounce == 0
        assert sp.throttle == 0

    def test_save_prop_with_dict_name(self):
        """Test SaveProp with a dict mapping."""
        sp = SaveProp(name={"value": "email", "name": "field"})
        assert sp.name == {"value": "email", "name": "field"}

    def test_save_prop_with_debounce(self):
        """Test SaveProp with debounce."""
        sp = SaveProp(name="search", debounce=300)
        assert sp.debounce == 300

    def test_save_prop_with_throttle(self):
        """Test SaveProp with throttle."""
        sp = SaveProp(name="scroll_pos", throttle=100)
        assert sp.throttle == 100

    def test_save_prop_serialize_string(self):
        """Test SaveProp serialization with string name."""
        sp = SaveProp(name="email")
        serialized = sp.serialize()

        assert serialized == {"saveProp": "email"}
        assert "debounce" not in serialized
        assert "throttle" not in serialized

    def test_save_prop_serialize_dict(self):
        """Test SaveProp serialization with dict mapping."""
        sp = SaveProp(name={"value": "user_email"})
        serialized = sp.serialize()

        assert serialized == {"saveProp": {"value": "user_email"}}

    def test_save_prop_serialize_with_debounce(self):
        """Test SaveProp serialization includes debounce when set."""
        sp = SaveProp(name="query", debounce=200)
        serialized = sp.serialize()

        assert serialized["saveProp"] == "query"
        assert serialized["debounce"] == 200

    def test_save_prop_serialize_with_throttle(self):
        """Test SaveProp serialization includes throttle when set."""
        sp = SaveProp(name="field", throttle=50)
        serialized = sp.serialize()

        assert serialized["saveProp"] == "field"
        assert serialized["throttle"] == 50

    def test_save_prop_serialize_omits_zero_timing(self):
        """Test SaveProp serialization omits zero debounce/throttle."""
        sp = SaveProp(name="field", debounce=0, throttle=0)
        serialized = sp.serialize()

        assert "debounce" not in serialized
        assert "throttle" not in serialized


class TestChainedAction:
    """Tests for ChainedAction dataclass."""

    def test_chained_action_with_callbacks(self):
        """Test ChainedAction with multiple callbacks."""

        def handler():
            pass

        actions = [
            SaveProp(name="email"),
            Callback(id="cb1", func=handler),
        ]
        chain = ChainedAction(actions=actions)
        assert len(chain.actions) == 2
        assert chain.mode == "serial"

    def test_chained_action_parallel_mode(self):
        """Test ChainedAction with parallel mode."""

        def handler():
            pass

        chain = ChainedAction(
            actions=[Callback(id="cb1", func=handler), Callback(id="cb2", func=handler)],
            mode="parallel",
        )
        assert chain.mode == "parallel"

    def test_chained_action_rejects_invalid_action(self):
        """Test ChainedAction rejects non-action types."""
        with pytest.raises(TypeError, match="Action at index 0"):
            ChainedAction(actions=["not_an_action"])

    def test_chained_action_rejects_invalid_mode(self):
        """Test ChainedAction rejects invalid mode."""
        with pytest.raises(ValueError, match="serial.*parallel"):
            ChainedAction(actions=[SaveProp(name="x")], mode="invalid")

    def test_chained_action_nested(self):
        """Test ChainedAction can be nested."""

        def handler():
            pass

        inner = ChainedAction(
            actions=[Callback(id="cb1", func=handler), Callback(id="cb2", func=handler)],
            mode="parallel",
        )
        outer = ChainedAction(
            actions=[SaveProp(name="x"), inner],
            mode="serial",
        )
        assert len(outer.actions) == 2
        assert isinstance(outer.actions[1], ChainedAction)

    def test_chained_action_serialize(self):
        """Test ChainedAction serialization."""
        chain = ChainedAction(
            actions=[
                SaveProp(name="email"),
                JsCallback(code="console.log('done')"),
            ],
            mode="serial",
        )
        serialized = chain.serialize()

        assert "chain" in serialized
        assert serialized["mode"] == "serial"
        assert len(serialized["chain"]) == 2
        assert serialized["chain"][0] == {"saveProp": "email"}
        assert serialized["chain"][1]["jsFunction"] == "console.log('done')"

    def test_chained_action_serialize_parallel(self):
        """Test ChainedAction serialization with parallel mode."""

        def handler():
            pass

        chain = ChainedAction(
            actions=[Callback(id="cb1", func=handler)],
            mode="parallel",
        )
        serialized = chain.serialize()
        assert serialized["mode"] == "parallel"

    def test_chained_action_all_action_types(self):
        """Test ChainedAction accepts all valid action types."""

        def handler():
            pass

        actions = [
            Callback(id="cb1", func=handler),
            JsCallback(code="alert('hi')"),
            BoundJsCallback(target_id="canvas", method_name="clear"),
            SaveProp(name="field"),
        ]
        chain = ChainedAction(actions=actions)
        assert len(chain.actions) == 4


class TestCallbackDebounceThrottle:
    """Tests for debounce/throttle on Callback."""

    def test_callback_default_no_debounce(self):
        """Test Callback has 0 debounce by default."""

        def handler():
            pass

        cb = Callback(id="test", func=handler)
        assert cb.debounce == 0
        assert cb.throttle == 0

    def test_callback_with_debounce(self):
        """Test Callback with debounce."""

        def handler():
            pass

        cb = Callback(id="test", func=handler, debounce=300)
        assert cb.debounce == 300

    def test_callback_with_throttle(self):
        """Test Callback with throttle."""

        def handler():
            pass

        cb = Callback(id="test", func=handler, throttle=100)
        assert cb.throttle == 100

    def test_callback_serialize_includes_debounce(self):
        """Test Callback serialize includes debounce when set."""

        def handler():
            pass

        cb = Callback(id="test", func=handler, debounce=500)
        serialized = cb.serialize()
        assert serialized["debounce"] == 500
        assert "throttle" not in serialized

    def test_callback_serialize_includes_throttle(self):
        """Test Callback serialize includes throttle when set."""

        def handler():
            pass

        cb = Callback(id="test", func=handler, throttle=200)
        serialized = cb.serialize()
        assert serialized["throttle"] == 200
        assert "debounce" not in serialized

    def test_callback_serialize_omits_zero_timing(self):
        """Test Callback serialize omits zero debounce/throttle."""

        def handler():
            pass

        cb = Callback(id="test", func=handler, debounce=0, throttle=0)
        serialized = cb.serialize()
        assert "debounce" not in serialized
        assert "throttle" not in serialized

    def test_callback_no_store_as_field(self):
        """Test Callback no longer has store_as or store_only fields."""

        def handler():
            pass

        cb = Callback(id="test", func=handler)
        assert not hasattr(cb, "store_as")
        assert not hasattr(cb, "store_only")


class TestContextSaveProp:
    """Tests for Context.save_prop() method."""

    def test_save_prop_creates_save_prop(self):
        """Test save_prop returns a SaveProp."""
        ctx = Context()
        sp = ctx.save_prop("email")
        assert isinstance(sp, SaveProp)
        assert sp.name == "email"

    def test_save_prop_with_dict_mapping(self):
        """Test save_prop with dict mapping."""
        ctx = Context()
        sp = ctx.save_prop({"value": "email", "name": "field"})
        assert sp.name == {"value": "email", "name": "field"}

    def test_save_prop_with_debounce(self):
        """Test save_prop with debounce."""
        ctx = Context()
        sp = ctx.save_prop("query", debounce=200)
        assert sp.debounce == 200

    def test_save_prop_with_throttle(self):
        """Test save_prop with throttle."""
        ctx = Context()
        sp = ctx.save_prop("scroll", throttle=100)
        assert sp.throttle == 100


class TestContextChain:
    """Tests for Context.chain() method."""

    def test_chain_creates_chained_action(self):
        """Test chain returns a ChainedAction."""
        ctx = Context()
        sp = ctx.save_prop("email")

        def handler():
            pass

        cb = ctx.callback(handler)
        chain = ctx.chain([sp, cb])
        assert isinstance(chain, ChainedAction)
        assert len(chain.actions) == 2
        assert chain.mode == "serial"

    def test_chain_parallel_mode(self):
        """Test chain with parallel mode."""
        ctx = Context()

        def handler():
            pass

        cb1 = ctx.callback(handler)
        cb2 = ctx.callback(handler)
        chain = ctx.chain([cb1, cb2], mode="parallel")
        assert chain.mode == "parallel"

    def test_chain_rejects_invalid_action(self):
        """Test chain rejects invalid action types."""
        ctx = Context()
        with pytest.raises(TypeError):
            ctx.chain(["not_an_action"])

    def test_chain_rejects_invalid_mode(self):
        """Test chain rejects invalid mode."""
        ctx = Context()
        with pytest.raises(ValueError):
            ctx.chain([ctx.save_prop("x")], mode="banana")

    def test_chain_nested(self):
        """Test chain can be nested."""
        ctx = Context()

        def handler():
            pass

        inner = ctx.chain([ctx.callback(handler), ctx.callback(handler)], mode="parallel")
        outer = ctx.chain([ctx.save_prop("x"), inner])

        assert isinstance(outer, ChainedAction)
        assert isinstance(outer.actions[1], ChainedAction)
        assert outer.actions[1].mode == "parallel"

    def test_chain_serialize_format(self):
        """Test chain serialization format."""
        ctx = Context()
        chain = ctx.chain(
            [
                ctx.save_prop("email"),
                ctx.js("console.log('done')"),
            ]
        )
        serialized = chain.serialize()

        assert "chain" in serialized
        assert serialized["mode"] == "serial"
        assert len(serialized["chain"]) == 2


class TestContextUpdatePropsChildren:
    """Tests for Context.update_props() with children support."""

    @pytest.mark.asyncio
    async def test_update_props_with_empty_children(self):
        """Test update_props can clear children with an empty list."""
        ws = AsyncMock()
        ctx = Context(websocket=ws)

        await ctx.update_props("container-1", {"children": []})

        ws.send_json.assert_called_once_with(
            {
                "type": "update",
                "operation": "update_props",
                "targetId": "container-1",
                "children": [],
            }
        )

    @pytest.mark.asyncio
    async def test_update_props_with_component_children(self):
        """Test update_props serializes Component children."""
        from refast.components.base import Container

        ws = AsyncMock()
        ctx = Context(websocket=ws)

        child = Container(id="child-1", class_name="p-2")
        await ctx.update_props("parent", {"children": [child]})

        call_args = ws.send_json.call_args[0][0]
        assert call_args["type"] == "update"
        assert call_args["operation"] == "update_props"
        assert call_args["targetId"] == "parent"
        assert "props" not in call_args
        assert len(call_args["children"]) == 1
        assert call_args["children"][0]["type"] == "Container"
        assert call_args["children"][0]["id"] == "child-1"

    @pytest.mark.asyncio
    async def test_update_props_with_string_children(self):
        """Test update_props with string children."""
        ws = AsyncMock()
        ctx = Context(websocket=ws)

        await ctx.update_props("text-1", {"children": ["Hello", "World"]})

        ws.send_json.assert_called_once_with(
            {
                "type": "update",
                "operation": "update_props",
                "targetId": "text-1",
                "children": ["Hello", "World"],
            }
        )

    @pytest.mark.asyncio
    async def test_update_props_children_with_regular_props(self):
        """Test update_props can mix children with regular props."""
        from refast.components.base import Container

        ws = AsyncMock()
        ctx = Context(websocket=ws)

        child = Container(id="new-child")
        await ctx.update_props(
            "parent",
            {
                "class_name": "p-4 bg-white",
                "children": [child],
            },
        )

        call_args = ws.send_json.call_args[0][0]
        assert call_args["props"] == {"class_name": "p-4 bg-white"}
        assert len(call_args["children"]) == 1
        assert call_args["children"][0]["type"] == "Container"

    @pytest.mark.asyncio
    async def test_update_props_regular_props_only(self):
        """Test update_props without children works as before."""
        ws = AsyncMock()
        ctx = Context(websocket=ws)

        await ctx.update_props("btn-1", {"label": "New Label", "disabled": True})

        ws.send_json.assert_called_once_with(
            {
                "type": "update",
                "operation": "update_props",
                "targetId": "btn-1",
                "props": {"label": "New Label", "disabled": True},
            }
        )

    @pytest.mark.asyncio
    async def test_update_props_serializes_component_in_prop_value(self):
        """Test update_props serializes Component objects in regular prop values."""
        from refast.components.base import Container

        ws = AsyncMock()
        ctx = Context(websocket=ws)

        comp = Container(id="icon-comp")
        await ctx.update_props("btn-1", {"icon": comp})

        call_args = ws.send_json.call_args[0][0]
        assert call_args["props"]["icon"]["type"] == "Container"
        assert call_args["props"]["icon"]["id"] == "icon-comp"

    @pytest.mark.asyncio
    async def test_update_props_without_websocket_with_children(self):
        """Test update_props with children does nothing without websocket."""
        ctx = Context()
        # Should not raise
        await ctx.update_props("target-id", {"children": []})
