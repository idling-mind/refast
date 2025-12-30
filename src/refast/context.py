"""Context class for request handling."""

import uuid
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Generic, TypeVar

from fastapi import Request, WebSocket

from refast.state import State

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
    """

    id: str
    func: Callable
    bound_args: dict[str, Any] = field(default_factory=dict)

    def serialize(self) -> dict[str, Any]:
        """Serialize for sending to frontend."""
        return {
            "callbackId": self.id,
            "boundArgs": self.bound_args,
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
            await ctx.push_update()
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
        self._session: Session | None = None
        self._event_data: dict[str, Any] = {}

    @property
    def event_data(self) -> dict[str, Any]:
        """Access the event data from a callback invocation."""
        return self._event_data

    def set_event_data(self, data: dict[str, Any]) -> None:
        """Set the event data (called by event manager)."""
        self._event_data = data

    @property
    def state(self) -> State:
        """Access the state object."""
        return self._state

    @property
    def session(self) -> "Session":
        """Access the session."""
        if self._session is None:
            from refast.session.session import Session

            self._session = Session()
        return self._session

    def callback(
        self,
        func: Callable,
        **bound_args: Any,
    ) -> Callback:
        """
        Create a callback that can be triggered from the frontend.

        Args:
            func: The function to call
            **bound_args: Arguments to bind to the callback

        Returns:
            Callback object that serializes for frontend

        Example:
            ```python
            Button(
                "Delete",
                on_click=ctx.callback(delete_item, item_id=item["id"])
            )
            ```
        """
        callback_id = str(uuid.uuid4())
        cb = Callback(id=callback_id, func=func, bound_args=bound_args)

        # Register with app
        if self._app:
            self._app.register_callback(callback_id, func)

        return cb

    async def push_update(self) -> None:
        """Push state updates to the frontend."""
        if self._websocket:
            await self._websocket.send_json(
                {
                    "type": "state_update",
                    "state": self._state.to_dict(),
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

    async def navigate(self, path: str) -> None:
        """Navigate to a different page."""
        if self._websocket:
            await self._websocket.send_json(
                {
                    "type": "navigate",
                    "path": path,
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
        duration: int = 3000,
    ) -> None:
        """Show a toast notification."""
        if self._websocket:
            await self._websocket.send_json(
                {
                    "type": "toast",
                    "message": message,
                    "variant": variant,
                    "duration": duration,
                }
            )

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
