"""Action types used in Refast event handlers.

These are the serializable value objects that represent frontend actions:
Python callbacks, JavaScript code, component method calls, prop-store writes,
and composed chains of the above.

All action types with timing fields (``debounce`` / ``throttle``) inherit from
:class:`_WithTiming` which provides the shared ``_serialize_timing()`` helper.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any


class _WithTiming:
    """Mixin for action dataclasses that support debounce/throttle.

    Subclasses must declare ``debounce: int = 0`` and ``throttle: int = 0``
    as dataclass fields; this mixin only provides the serialization helper.
    """

    debounce: int
    throttle: int

    def _serialize_timing(self) -> dict[str, Any]:
        result: dict[str, Any] = {}
        if self.debounce > 0:
            result["debounce"] = self.debounce
        if self.throttle > 0:
            result["throttle"] = self.throttle
        return result


@dataclass
class Callback(_WithTiming):
    """
    Represents a callback that can be triggered from the frontend.

    Callbacks are serializable references to Python functions that
    the frontend can invoke via WebSocket.

    The `props` parameter specifies which prop store values to include:
    - Only requested props are sent with the callback (not the entire store)
    - Values are passed as keyword arguments to the callback function

    Example:
        ```python
        # Use with ctx.save_prop to capture input and send on submit
        Input(on_change=ctx.save_prop("email"))
        Input(on_change=ctx.save_prop("name"))

        # Request specific props - they come as kwargs
        Button(on_click=ctx.callback(submit, props=["email", "name"]))

        async def submit(ctx, email: str, name: str):
            print(f"Email: {email}, Name: {name}")

        # With debounce (in milliseconds)
        Input(on_change=ctx.callback(search, debounce=300))
        ```
    """

    id: str
    func: Callable[..., Any]
    bound_args: dict[str, Any] = field(default_factory=dict)
    props: list[str] | None = None
    debounce: int = 0
    throttle: int = 0

    def serialize(self) -> dict[str, Any]:
        """Serialize for sending to frontend."""
        result: dict[str, Any] = {
            "callbackId": self.id,
            "boundArgs": self.bound_args,
        }
        if self.props is not None:
            result["props"] = self.props
        result.update(self._serialize_timing())
        return result


@dataclass
class JsCallback(_WithTiming):
    """
    Represents a JavaScript function to be executed on the frontend.

    Unlike regular Callbacks which invoke Python functions via WebSocket,
    JsCallbacks execute JavaScript code directly in the browser without
    a server roundtrip.

    The JavaScript function receives an event object with the following structure:
    - For DOM events: { value, checked, name, target, ... }
    - For custom callbacks: the data passed to the callback

    Example:
        ```python
        # Simple alert
        Button("Click me", on_click=ctx.js("alert('Hello!')"))

        # Toggle a class
        Button("Toggle", on_click=ctx.js("document.body.classList.toggle('dark')"))

        # Access event data
        Input(on_change=ctx.js("console.log('Value:', event.value)"))

        # Call a global function
        Button("Save", on_click=ctx.js("window.myApp.save()"))

        # With bound arguments
        Button("Delete", on_click=ctx.js("deleteItem(args.itemId)", item_id=123))
        ```

    Attributes:
        code: JavaScript code to execute
        bound_args: Arguments available as 'args' object in the JS code
        debounce: Milliseconds to debounce execution
        throttle: Milliseconds to throttle execution
    """

    code: str
    bound_args: dict[str, Any] = field(default_factory=dict)
    debounce: int = 0
    throttle: int = 0

    @staticmethod
    def _serialize_bound_args(bound_args: dict[str, Any]) -> dict[str, Any]:
        """Serialize bound args, converting Callback objects to their serialized form."""
        result: dict[str, Any] = {}
        for key, value in bound_args.items():
            if hasattr(value, "serialize") and callable(value.serialize):
                result[key] = value.serialize()
            else:
                result[key] = value
        return result

    def serialize(self) -> dict[str, Any]:
        """Serialize for sending to frontend."""
        result: dict[str, Any] = {
            "jsFunction": self.code,
            "boundArgs": self._serialize_bound_args(self.bound_args),
        }
        result.update(self._serialize_timing())
        return result


@dataclass
class JsAction:
    """
    Represents a JavaScript action to be sent to the frontend for execution.

    Used by ctx.call_js() to execute JavaScript code on the client.

    Attributes:
        code: JavaScript code to execute
        args: Arguments passed to the JavaScript code
    """

    code: str
    args: dict[str, Any] = field(default_factory=dict)


@dataclass
class BoundJsCallback(_WithTiming):
    """
    Represents a bound method call to be executed on a component in the frontend.

    Unlike JsCallback which executes arbitrary JavaScript code,
    BoundJsCallback calls a specific method on a component identified by its ID.
    This is useful for calling component methods without a server roundtrip.

    Example:
        ```python
        # Call clearCanvas method on a SketchCanvas component
        Button("Clear", on_click=ctx.bound_js("my-canvas", "clearCanvas"))

        # Call a method with positional arguments
        Button("Set Size", on_click=ctx.bound_js("my-canvas", "setSize", 800, 600))

        # Call a method with keyword arguments
        Button("Load", on_click=ctx.bound_js("my-canvas", "loadPaths", paths=my_paths))

        # Call a method with both positional and keyword arguments
        Button("Draw", on_click=ctx.bound_js("my-canvas", "draw", "circle", x=100, y=200))

        # Toggle eraser mode
        Button("Eraser", on_click=ctx.bound_js("my-canvas", "eraseMode", True))
        ```

    Attributes:
        target_id: ID of the target component
        method_name: Name of the method to call on the component
        args: Positional arguments to pass to the method
        kwargs: Keyword arguments to pass to the method
        debounce: Milliseconds to debounce execution
        throttle: Milliseconds to throttle execution
    """

    target_id: str
    method_name: str
    args: tuple[Any, ...] = field(default_factory=tuple)
    kwargs: dict[str, Any] = field(default_factory=dict)
    debounce: int = 0
    throttle: int = 0

    def serialize(self) -> dict[str, Any]:
        """Serialize for sending to frontend."""
        result: dict[str, Any] = {
            "boundMethod": {
                "targetId": self.target_id,
                "methodName": self.method_name,
                "args": list(self.args),
                "kwargs": self.kwargs,
            }
        }
        result.update(self._serialize_timing())
        return result


@dataclass
class SaveProp(_WithTiming):
    """
    Stores event data in the frontend prop store without a server roundtrip.

    This is a first-class action that captures event values on the frontend.
    Use it to collect input values that can later be sent with a Callback
    via the ``props`` parameter.

    Args:
        name: Store key or mapping. Can be:
            - str: Store the event's "value" under this key
            - dict: Map event data keys to store keys
              (e.g., {"value": "email", "name": "field_name"})
        debounce: Milliseconds to debounce the store write
        throttle: Milliseconds to throttle the store write

    Example:
        ```python
        # Store input value as "email" in prop store
        Input(on_change=ctx.save_prop("email"))

        # Map multiple event fields to store keys
        Input(on_change=ctx.save_prop({"value": "email", "name": "field"}))

        # Combine with a callback using ctx.chain
        Input(
            on_change=ctx.chain([
                ctx.save_prop("email"),
                ctx.callback(validate_email, props=["email"]),
            ])
        )
        ```
    """

    name: str | dict[str, str]
    debounce: int = 0
    throttle: int = 0

    def serialize(self) -> dict[str, Any]:
        """Serialize for sending to frontend."""
        result: dict[str, Any] = {"saveProp": self.name}
        result.update(self._serialize_timing())
        return result


@dataclass
class ChainedAction:
    """
    Composes multiple actions to fire on a single event.

    Actions are executed in order (serial) or simultaneously (parallel).
    Chains can be nested — a ChainedAction can contain other ChainedActions.

    Args:
        actions: List of actions to execute. Each must be a Callback,
            JsCallback, BoundJsCallback, SaveProp, or another ChainedAction.
        mode: Execution mode — "serial" (default) or "parallel".
            - "serial": Each action completes before the next starts.
            - "parallel": All actions fire simultaneously.

    Example:
        ```python
        # Store value AND call a server function
        Input(
            on_change=ctx.chain([
                ctx.save_prop("search"),
                ctx.callback(do_search, props=["search"], debounce=300),
            ])
        )

        # Mix JS and Python actions
        Button(
            "Submit",
            on_click=ctx.chain([
                ctx.js("showSpinner()"),
                ctx.callback(handle_submit, props=["email", "name"]),
            ])
        )

        # Nested chains with different modes
        Button(
            "Save All",
            on_click=ctx.chain([
                ctx.js("showLoading()"),
                ctx.chain([
                    ctx.callback(save_draft),
                    ctx.callback(save_settings),
                ], mode="parallel"),
            ])
        )
        ```
    """

    actions: list[Any]  # list of Callback | JsCallback | BoundJsCallback | SaveProp | ChainedAction
    mode: str = "serial"  # "serial" or "parallel"

    def __post_init__(self) -> None:
        """Validate actions and mode."""
        valid_types = (Callback, JsCallback, BoundJsCallback, SaveProp, ChainedAction)
        for i, action in enumerate(self.actions):
            if not isinstance(action, valid_types):
                raise TypeError(
                    f"Action at index {i} is {type(action).__name__}, "
                    f"expected one of: Callback, JsCallback, BoundJsCallback, "
                    f"SaveProp, ChainedAction"
                )
        if self.mode not in ("serial", "parallel"):
            raise ValueError(f"mode must be 'serial' or 'parallel', got {self.mode!r}")

    def serialize(self) -> dict[str, Any]:
        """Serialize for sending to frontend."""
        return {
            "chain": [action.serialize() for action in self.actions],
            "mode": self.mode,
        }


# Union type for all action types that can be used in event handlers
ActionType = Callback | JsCallback | BoundJsCallback | SaveProp | ChainedAction
