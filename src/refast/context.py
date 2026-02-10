"""Context class for request handling."""

import asyncio
import uuid
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Generic, TypeVar

from fastapi import Request, WebSocket

from refast.state import State
from refast.store import Store

if TYPE_CHECKING:
    from refast.app import RefastApp
    from refast.session.session import Session

T = TypeVar("T")


@dataclass
class Callback:
    """
    Represents a callback that can be triggered from the frontend.

    Callbacks are serializable references to Python functions that
    the frontend can invoke via WebSocket.

    The `store_as` parameter enables frontend-only state storage:
    - When specified, event values are stored in the prop store
    - Stored values are available to all subsequent callbacks
    - Avoids server roundtrips for input state synchronization

    The `props` parameter specifies which prop store values to include:
    - Only requested props are sent with the callback (not the entire store)
    - Values are passed as keyword arguments to the callback function

    Example:
        ```python
        # Store input value as "email" in prop store (no server call)
        Input(on_change=ctx.callback(store_as="email"))
        Input(on_change=ctx.callback(store_as="name"))

        # Request specific props - they come as kwargs
        Button(on_click=ctx.callback(submit, props=["email", "name"]))

        async def submit(ctx, email: str, name: str):
            # email and name are passed directly!
            print(f"Email: {email}, Name: {name}")
        ```
    """

    id: str
    func: Callable | None
    bound_args: dict[str, Any] = field(default_factory=dict)
    store_as: str | dict[str, str] | None = None
    store_only: bool = False
    props: list[str] | None = None

    def serialize(self) -> dict[str, Any]:
        """Serialize for sending to frontend."""
        result = {
            "callbackId": self.id,
            "boundArgs": self.bound_args,
        }
        if self.store_as is not None:
            result["storeAs"] = self.store_as
        if self.store_only:
            result["storeOnly"] = True
        if self.props is not None:
            result["props"] = self.props
        return result


@dataclass
class JsCallback:
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
    """

    code: str
    bound_args: dict[str, Any] = field(default_factory=dict)

    def serialize(self) -> dict[str, Any]:
        """Serialize for sending to frontend."""
        return {
            "jsFunction": self.code,
            "boundArgs": self.bound_args,
        }


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
class BoundJsCallback:
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
    """

    target_id: str
    method_name: str
    args: tuple[Any, ...] = field(default_factory=tuple)
    kwargs: dict[str, Any] = field(default_factory=dict)

    def serialize(self) -> dict[str, Any]:
        """Serialize for sending to frontend."""
        return {
            "boundMethod": {
                "targetId": self.target_id,
                "methodName": self.method_name,
                "args": list(self.args),
                "kwargs": self.kwargs,
            }
        }


class Context(Generic[T]):
    """
    Request context passed to page functions and callbacks.

    Provides access to:
    - State management
    - Session data
    - Component update methods
    - Callback creation

    Example:
        ```python
        @ui.page("/")
        def home(ctx: Context):
            count = ctx.state.get("count", 0)
            return Button(
                f"Count: {count}",
                on_click=ctx.callback(increment, amount=1)
            )

        async def increment(ctx: Context, amount: int):
            ctx.state["count"] = ctx.state.get("count", 0) + amount
            await ctx.refresh()
        ```
    """

    def __init__(
        self,
        request: Request | None = None,
        websocket: WebSocket | None = None,
        app: "RefastApp | None" = None,
    ):
        self._request = request
        self._websocket = websocket
        self._app = app
        self._state: State = State()
        self._store: Store | None = None
        self._session: Session | None = None
        self._event_data: dict[str, Any] = {}
        self._prop_store: dict[str, Any] = {}
        self._store_sync_future: asyncio.Future[None] | None = None

    @property
    def event_data(self) -> dict[str, Any]:
        """Access the event data from a callback invocation."""
        return self._event_data

    def set_event_data(self, data: dict[str, Any]) -> None:
        """Set the event data (called by event manager)."""
        self._event_data = data

    @property
    def prop_store(self) -> dict[str, Any]:
        """
        Access values stored from component events via store_as.

        The prop store is a frontend-only key-value store that captures
        values from component events (like input changes) without requiring
        server roundtrips. Values are sent to the backend only when a
        callback is invoked.

        Example:
            ```python
            # In page function, set up store_as for inputs
            Input(on_change=ctx.callback(store_as="email"))
            Input(on_change=ctx.callback(store_as="username"))

            # In callback, access stored values
            async def submit(ctx):
                email = ctx.prop_store.get("email", "")
                username = ctx.prop_store.get("username", "")
            ```

        Returns:
            Dict containing all values stored via store_as directives
        """
        return self._prop_store

    def set_prop_store(self, data: dict[str, Any]) -> None:
        """Set the prop store data (called by event manager)."""
        self._prop_store = data

    @property
    def state(self) -> State:
        """Access the state object."""
        return self._state

    @property
    def store(self) -> Store:
        """
        Access browser storage (localStorage and sessionStorage).

        Use `ctx.store.local` for localStorage (persists across restarts).
        Use `ctx.store.session` for sessionStorage (persists until tab closes).

        Example:
            ```python
            # localStorage - persists across browser restarts
            theme = ctx.store.local.get("theme", "light")
            ctx.store.local.set("theme", "dark")

            # sessionStorage - persists until tab is closed
            ctx.store.session.set("wizard_step", 2)
            ```
        """
        if self._store is None:
            self._store = Store(self)
        return self._store

    @property
    def session(self) -> "Session":
        """Access the session."""
        if self._session is None:
            from refast.session.session import Session

            self._session = Session()
        return self._session

    def callback(
        self,
        func: Callable | None = None,
        *,
        store_as: str | dict[str, str] | None = None,
        props: list[str] | None = None,
        **bound_args: Any,
    ) -> Callback:
        """
        Create a callback that can be triggered from the frontend.

        Args:
            func: The function to call (optional if store_as is provided)
            store_as: Store event data in the prop store. Can be:
                - str: Store event's "value" under this key
                - dict: Map event data keys to store keys (e.g., {"value": "email"})
            props: List of prop store keys to include with this callback.
                Values are passed as keyword arguments to the function.
            **bound_args: Arguments to bind to the callback

        Returns:
            Callback object that serializes for frontend

        Example:
            ```python
            # Store-only callback (no server roundtrip)
            Input(on_change=ctx.callback(store_as="email"))
            Input(on_change=ctx.callback(store_as="name"))

            # Request specific props - they come as kwargs
            Button(
                "Submit",
                on_click=ctx.callback(handle_submit, props=["email", "name"])
            )

            async def handle_submit(ctx, email: str, name: str):
                # Props are passed directly as arguments!
                print(f"Email: {email}, Name: {name}")
            ```
        """
        callback_id = str(uuid.uuid4())
        store_only = func is None and store_as is not None

        cb = Callback(
            id=callback_id,
            func=func,
            bound_args=bound_args,
            store_as=store_as,
            store_only=store_only,
            props=props,
        )

        # Register with app (only if there's a function to call)
        if self._app and func is not None:
            self._app.register_callback(callback_id, func)

        return cb

    def js(
        self,
        code: str,
        **bound_args: Any,
    ) -> JsCallback:
        """
        Create a JavaScript callback that executes on the frontend.

        Unlike `callback()` which invokes a Python function via WebSocket,
        `js()` executes JavaScript code directly in the browser without
        a server roundtrip. This is useful for:

        - UI interactions that don't need server state (toggling classes, animations)
        - Calling existing JavaScript libraries or global functions
        - Performance-critical interactions that need immediate response
        - Simple client-side logic

        The JavaScript code has access to:
        - `event`: The event data object (value, checked, name, etc.)
        - `args`: The bound arguments passed to js()
        - `element`: The DOM element that triggered the event (if applicable)

        Args:
            code: JavaScript code to execute
            **bound_args: Arguments available as `args` in the JS code

        Returns:
            JsCallback object that serializes for frontend

        Example:
            ```python
            # Simple alert
            Button("Alert", on_click=ctx.js("alert('Hello!')"))

            # Toggle dark mode
            Button(
                "Toggle Theme",
                on_click=ctx.js("document.body.classList.toggle('dark')")
            )

            # Access event value
            Input(on_change=ctx.js("console.log('Input:', event.value)"))

            # With bound arguments
            Button(
                "Delete",
                on_click=ctx.js("deleteItem(args.itemId)", item_id=123)
            )

            # Call global functions
            Button("Save", on_click=ctx.js("window.myApp.save(args.data)", data=my_data))

            # Combine with Python callback - JS runs first, then Python
            Button(
                "Submit",
                on_click=ctx.js("validateForm() && true")  # Use Python callback for real action
            )
            ```

        Note:
            For security, avoid using user-provided strings in `code`.
            Bound arguments are properly serialized and safe to use.
        """
        return JsCallback(code=code, bound_args=bound_args)

    def bound_js(
        self,
        target_id: str,
        method_name: str,
        *args: Any,
        **kwargs: Any,
    ) -> BoundJsCallback:
        """
        Create a bound method callback that calls a component method on the frontend.

        Unlike `js()` which executes arbitrary JavaScript code,
        `bound_js()` calls a specific method on a component identified by its ID.
        This is useful for:

        - Calling component-specific methods (e.g., clearCanvas, undo, redo)
        - Interacting with components that expose imperative methods
        - Client-side operations without server roundtrip

        Components must expose methods by binding them to the wrapper DOM element.
        See the Component Development Guide for how to properly expose methods.

        Args:
            target_id: ID of the target component
            method_name: Name of the method to call
            *args: Positional arguments to pass to the method
            **kwargs: Keyword arguments to pass to the method

        Returns:
            BoundJsCallback object that serializes for frontend

        Example:
            ```python
            # Create a SketchCanvas with an ID
            canvas = SketchCanvas(id="my-canvas")

            # Call component methods without server roundtrip
            Button("Clear", on_click=ctx.bound_js("my-canvas", "clearCanvas"))
            Button("Undo", on_click=ctx.bound_js("my-canvas", "undo"))
            Button("Redo", on_click=ctx.bound_js("my-canvas", "redo"))

            # Call a method with positional argument
            Button(
                "Eraser On",
                on_click=ctx.bound_js("my-canvas", "eraseMode", True)
            )
            Button(
                "Eraser Off",
                on_click=ctx.bound_js("my-canvas", "eraseMode", False)
            )

            # Call a method with keyword arguments
            Button(
                "Load Drawing",
                on_click=ctx.bound_js("my-canvas", "loadPaths", paths=saved_paths)
            )

            # Call a method with both positional and keyword arguments
            Button(
                "Draw Circle",
                on_click=ctx.bound_js("my-canvas", "drawShape", "circle", x=100, y=200)
            )
            ```

        Note:
            The target component must have the method bound to its wrapper element.
            If the method or component doesn't exist, a warning will be logged.
        """
        return BoundJsCallback(
            target_id=target_id, method_name=method_name, args=args, kwargs=kwargs
        )

    async def call_js(
        self,
        code: str,
        **args: Any,
    ) -> None:
        """
        Execute JavaScript code on the frontend immediately.

        Unlike `js()` which creates a callback for event handlers,
        `call_js()` sends JavaScript to the frontend for immediate execution.
        This is useful for:

        - Triggering animations or transitions after state changes
        - Interacting with third-party JavaScript libraries
        - Scrolling, focusing, or other DOM manipulations
        - Executing custom client-side logic from a Python callback

        The JavaScript code has access to:
        - `args`: The arguments passed to call_js()

        Args:
            code: JavaScript code to execute
            **args: Arguments available as `args` in the JS code

        Example:
            ```python
            async def save_complete(ctx: Context):
                # Save to database...
                ctx.state.set("saved", True)
                await ctx.refresh()

                # Trigger confetti animation
                await ctx.call_js("confetti({ particleCount: 100 })")

                # Scroll to top
                await ctx.call_js("window.scrollTo({ top: 0, behavior: 'smooth' })")

                # Focus an input
                await ctx.call_js(
                    "document.getElementById(args.inputId)?.focus()",
                    input_id="search-input"
                )
            ```

        Note:
            For security, avoid using user-provided strings in `code`.
            Arguments are properly serialized and safe to use.
        """
        if self._websocket:
            await self._websocket.send_json(
                {
                    "type": "js_exec",
                    "code": code,
                    "args": args,
                }
            )

    async def call_bound_js(
        self,
        target_id: str,
        method_name: str,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """
        Call a method on a component in the frontend immediately.

        Unlike `bound_js()` which creates a callback for event handlers,
        `call_bound_js()` sends a method call to the frontend for immediate execution.
        This is useful for:

        - Calling component methods after server-side processing
        - Triggering component actions in response to data changes
        - Imperatively controlling components from Python callbacks

        Args:
            target_id: ID of the target component
            method_name: Name of the method to call
            *args: Positional arguments to pass to the method
            **kwargs: Keyword arguments to pass to the method

        Example:
            ```python
            async def save_drawing(ctx: Context):
                # Export the paths from the canvas
                # (In a real app, you'd need to use a different approach
                # since exportPaths returns a Promise)
                await ctx.call_bound_js("my-canvas", "clearCanvas")

            async def load_saved_drawing(ctx: Context):
                # Load paths from database
                saved_paths = await database.get_drawing(ctx.event_data["id"])

                # Load the paths into the canvas
                await ctx.call_bound_js("my-canvas", "loadPaths", paths=saved_paths)

            async def toggle_eraser(ctx: Context):
                is_eraser = ctx.state.get("eraser_mode", False)
                ctx.state.set("eraser_mode", not is_eraser)
                await ctx.refresh()

                # Update the canvas mode (positional arg)
                await ctx.call_bound_js("my-canvas", "eraseMode", not is_eraser)

            async def draw_shape(ctx: Context):
                # Call with both positional and keyword arguments
                await ctx.call_bound_js("my-canvas", "drawShape", "circle", x=100, y=200)
            ```

        Note:
            The target component must have the method bound to its wrapper element.
            If the method or component doesn't exist, a warning will be logged.
        """
        if self._websocket:
            await self._websocket.send_json(
                {
                    "type": "bound_method_call",
                    "targetId": target_id,
                    "methodName": method_name,
                    "args": list(args),
                    "kwargs": kwargs,
                }
            )


    async def replace(self, target_id: str, component: Any) -> None:
        """Replace a component in the frontend."""
        if self._websocket:
            await self._websocket.send_json(
                {
                    "type": "update",
                    "operation": "replace",
                    "targetId": target_id,
                    "component": component.render() if hasattr(component, "render") else component,
                }
            )

    async def append(self, target_id: str, component: Any) -> None:
        """Append a component to a container."""
        if self._websocket:
            await self._websocket.send_json(
                {
                    "type": "update",
                    "operation": "append",
                    "targetId": target_id,
                    "component": component.render() if hasattr(component, "render") else component,
                }
            )

    async def prepend(self, target_id: str, component: Any) -> None:
        """Prepend a component to a container."""
        if self._websocket:
            await self._websocket.send_json(
                {
                    "type": "update",
                    "operation": "prepend",
                    "targetId": target_id,
                    "component": component.render() if hasattr(component, "render") else component,
                }
            )

    async def remove(self, target_id: str) -> None:
        """Remove a component from the frontend."""
        if self._websocket:
            await self._websocket.send_json(
                {
                    "type": "update",
                    "operation": "remove",
                    "targetId": target_id,
                }
            )

    async def update_props(self, target_id: str, props: dict[str, Any]) -> None:
        """Update props of an existing component."""
        if self._websocket:
            await self._websocket.send_json(
                {
                    "type": "update",
                    "operation": "update_props",
                    "targetId": target_id,
                    "props": props,
                }
            )

    async def update_text(self, target_id: str, text: str) -> None:
        """Update the text content of a component."""
        if self._websocket:
            await self._websocket.send_json(
                {
                    "type": "update",
                    "operation": "update_children",
                    "targetId": target_id,
                    "children": [text],
                }
            )

    async def append_prop(
        self,
        target_id: str,
        prop_name: str,
        value: Any,
    ) -> None:
        """
        Append a value to a component's prop.

        For string props (like 'content' in Markdown), the value is concatenated.
        For list/array props (like 'data' in charts), the value is appended or extended.

        This is useful for streaming scenarios where you want to incrementally
        update a component without replacing the entire prop value.

        Args:
            target_id: ID of the target component
            prop_name: Name of the prop to append to
            value: Value to append (string for concatenation, any for list append)

        Example:
            ```python
            # Streaming text to a Markdown component
            async def stream_response(ctx: Context):
                await ctx.update_props("output", {"streaming": True})

                async for chunk in llm_stream():
                    await ctx.append_prop("output", "content", chunk)

                await ctx.update_props("output", {"streaming": False})

            # Appending data points to a chart
            async def add_data_point(ctx: Context):
                new_point = {"x": time.time(), "y": sensor.read()}
                await ctx.append_prop("my-chart", "data", new_point)

            # Extending chart data with multiple points
            async def add_batch_data(ctx: Context):
                new_points = [{"x": i, "y": v} for i, v in enumerate(values)]
                await ctx.append_prop("my-chart", "data", new_points)
            ```
        """
        if self._websocket:
            await self._websocket.send_json(
                {
                    "type": "update",
                    "operation": "append_prop",
                    "targetId": target_id,
                    "propName": prop_name,
                    "value": value,
                }
            )

    async def navigate(self, path: str) -> None:
        """Navigate to a different page.

        Sends a navigate message to update the browser URL, then renders
        the target page and sends the component tree so the client
        displays the new content without a full page reload.

        Args:
            path: The target page path (e.g. "/docs/getting-started").
        """
        if self._websocket:
            await self._websocket.send_json(
                {
                    "type": "navigate",
                    "path": path,
                }
            )
            # Also render the target page and send its component tree
            if self._app:
                page_func = self._app._pages.get(path)
                if page_func is None:
                    page_func = self._app._pages.get("/")  # Fallback to index
                if page_func is not None:
                    component = page_func(self)
                    component_data = component.render() if hasattr(component, "render") else {}
                    await self._websocket.send_json(
                        {
                            "type": "page_render",
                            "component": component_data,
                        }
                    )

    async def refresh(self, path: str | None = None) -> None:
        """
        Refresh the current page by re-rendering it.

        This re-renders the page with the current state and sends the
        updated component tree directly via WebSocket, preserving state.

        Args:
            path: Optional path to refresh. If not provided, uses "/" as default.
        """
        if self._websocket and self._app:
            # Default to root path if not specified
            page_path = path or "/"

            # Find and render the page
            page_func = self._app._pages.get(page_path)
            if page_func is None:
                page_func = self._app._pages.get("/")  # Fallback to index

            if page_func is not None:
                # Re-render the page with current state
                component = page_func(self)
                component_data = component.render() if hasattr(component, "render") else {}

                # Send the rendered component tree via WebSocket
                await self._websocket.send_json(
                    {
                        "type": "refresh",
                        "component": component_data,
                    }
                )

    async def show_toast(
        self,
        message: str,
        variant: str = "default",
        description: str | None = None,
        duration: int | None = None,
        position: str | None = None,
        dismissible: bool = True,
        close_button: bool | None = None,
        invert: bool = False,
        action: dict | None = None,
        cancel: dict | None = None,
        toast_id: str | None = None,
    ) -> None:
        """
        Show a toast notification using Sonner.

        Args:
            message: The main message to display
            variant: Toast variant - "default", "success", "error", "warning", "info", "loading"
            description: Optional description text below the message
            duration: Duration in milliseconds (default: 4000, use float('inf') for persistent)
            position: Override position - "top-left", "top-center", "top-right",
                     "bottom-left", "bottom-center", "bottom-right"
            dismissible: Whether the toast can be dismissed by clicking (default: True)
            close_button: Whether to show a close button
            invert: Whether to invert the colors
            action: Action button config - {"label": str, "callback_id": str}
            cancel: Cancel button config - {"label": str, "callback_id": str}
            toast_id: Custom ID for the toast (useful for updating/dismissing)

        Example:
            # Simple toast
            await ctx.show_toast("Hello!")

            # Success toast with description
            await ctx.show_toast(
                "Saved!",
                variant="success",
                description="Your changes have been saved."
            )

            # Toast with action button
            await ctx.show_toast(
                "File deleted",
                action={"label": "Undo", "callback_id": "undo_delete"}
            )

            # Loading toast
            await ctx.show_toast("Processing...", variant="loading", toast_id="process")
            # Later, update it:
            await ctx.show_toast("Done!", variant="success", toast_id="process")
        """
        if self._websocket:
            payload: dict = {
                "type": "toast",
                "message": message,
                "variant": variant,
                "dismissible": dismissible,
                "invert": invert,
            }

            # Only include optional fields if provided
            if description is not None:
                payload["description"] = description
            if duration is not None:
                payload["duration"] = duration
            if position is not None:
                payload["position"] = position
            if close_button is not None:
                payload["close_button"] = close_button
            if action is not None:
                payload["action"] = action
            if cancel is not None:
                payload["cancel"] = cancel
            if toast_id is not None:
                payload["id"] = toast_id

            await self._websocket.send_json(payload)

    async def push_event(self, event_type: str, data: Any) -> None:
        """Push an event to the frontend."""
        if self._websocket:
            await self._websocket.send_json(
                {
                    "type": "event",
                    "eventType": event_type,
                    "data": data,
                }
            )

    async def set_theme(self, theme: Any) -> None:
        """
        Apply a new theme at runtime, pushing CSS variable overrides to the client.

        The theme is applied immediately on all connected clients (via WebSocket).
        The app-level ``theme`` is also updated so that future HTTP page loads
        use the new theme.

        Args:
            theme: A ``Theme`` instance (from ``refast.theme``).

        Example:
            ```python
            from refast.theme import rose_theme

            async def switch_to_rose(ctx: Context):
                await ctx.set_theme(rose_theme)
            ```
        """
        # Update the app-level theme for future page loads
        if self._app:
            self._app.theme = theme

        # Push the theme to the current client
        if self._websocket:
            await self._websocket.send_json(
                {
                    "type": "theme_update",
                    "theme": theme.to_dict(),
                }
            )

    async def broadcast_theme(self, theme: Any) -> int:
        """
        Broadcast a theme change to **all** connected clients.

        Args:
            theme: A ``Theme`` instance (from ``refast.theme``).

        Returns:
            Number of clients that received the update.

        Example:
            ```python
            from refast.theme import violet_theme

            async def set_global_theme(ctx: Context):
                await ctx.broadcast_theme(violet_theme)
            ```
        """
        if self._app:
            self._app.theme = theme

        if not self._app:
            return 0

        count = 0
        payload = {
            "type": "theme_update",
            "theme": theme.to_dict(),
        }
        for other_ctx in self._app.active_contexts:
            if other_ctx._websocket:
                try:
                    await other_ctx._websocket.send_json(payload)
                    count += 1
                except Exception:
                    pass
        return count

    async def broadcast(self, event_type: str, data: Any) -> int:
        """
        Broadcast an event to all connected clients.

        Args:
            event_type: Type of event to broadcast
            data: Event data to send

        Returns:
            Number of clients that received the broadcast
        """
        if not self._app:
            return 0

        count = 0
        for ctx in self._app.active_contexts:
            if ctx._websocket and ctx._websocket != self._websocket:
                try:
                    await ctx._websocket.send_json(
                        {
                            "type": "event",
                            "eventType": event_type,
                            "data": data,
                        }
                    )
                    count += 1
                except Exception:
                    # Connection may be closed
                    pass
        return count

    async def sync_store(self) -> None:
        """
        Sync any pending store updates to the browser.

        Note: Store updates are automatically synced when you modify
        values via `ctx.store.local` or `ctx.store.session`. You typically
        don't need to call this method manually.

        This method is called automatically:
        - After any store modification (set, delete, clear)
        - After callback invocations

        You may need to call this manually only in edge cases where
        the automatic sync doesn't work (e.g., no running event loop).
        """
        if self._websocket and self._store:
            updates = self._store._get_all_pending_updates()
            if updates:
                await self._websocket.send_json(
                    {
                        "type": "store_update",
                        "updates": updates,
                    }
                )

    async def _sync_store_from_browser(self, timeout: float = 2.0) -> None:
        """
        Request the browser to send its current storage state.

        This is called by store.sync() to refresh the cache with
        the latest browser values, including any JS changes.

        Args:
            timeout: Maximum time to wait for the browser response (seconds)
        """
        if not self._websocket:
            return  # No websocket, nothing to sync

        # Create a future to wait for the sync response
        loop = asyncio.get_event_loop()
        self._store_sync_future = loop.create_future()

        # Request the browser to send its current storage state
        await self._websocket.send_json({"type": "resync_store"})

        # Wait for the response with timeout
        try:
            await asyncio.wait_for(self._store_sync_future, timeout=timeout)
        except TimeoutError:
            # Log warning but don't fail - use cached values
            pass
        finally:
            self._store_sync_future = None

    def _resolve_store_sync(self) -> None:
        """
        Resolve the pending store sync future.

        Called internally when the browser sends a store_sync response.
        """
        if self._store_sync_future and not self._store_sync_future.done():
            self._store_sync_future.set_result(None)

    def _load_store_from_browser(self, data: dict[str, dict[str, str]]) -> None:
        """
        Load store data received from browser.

        Called internally when browser sends its storage state on connect.

        Args:
            data: Dictionary with "local" and "session" storage data
        """
        self.store._load_from_browser(data)
