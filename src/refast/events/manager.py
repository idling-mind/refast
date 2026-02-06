"""Event manager for routing events."""

import asyncio
import logging
from collections import defaultdict
from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any

from refast.events.types import Event, EventHandler

if TYPE_CHECKING:
    from refast.app import RefastApp
    from refast.context import Context

logger = logging.getLogger(__name__)


class EventManager:
    """
    Central event manager that routes events to handlers.

    Supports:
    - Event handler registration
    - Callback invocation
    - Event middleware
    - Error handling

    Example:
        ```python
        manager = EventManager()

        @manager.on("user:login")
        async def handle_login(ctx, event):
            print(f"User logged in: {event.data}")

        await manager.emit("user:login", {"user_id": 123})
        ```
    """

    def __init__(self, app: "RefastApp | None" = None):
        """
        Initialize the event manager.

        Args:
            app: Optional RefastApp instance
        """
        self.app = app
        self._handlers: dict[str, list[EventHandler]] = defaultdict(list)
        self._callbacks: dict[str, Callable[..., Any]] = {}
        self._middleware: list[Callable[..., Any]] = []

    def on(self, event_type: str) -> Callable[[EventHandler], EventHandler]:
        """
        Decorator to register an event handler.

        Args:
            event_type: The event type to handle

        Returns:
            Decorator function
        """

        def decorator(func: EventHandler) -> EventHandler:
            self._handlers[event_type].append(func)
            return func

        return decorator

    def register_handler(self, event_type: str, handler: EventHandler) -> None:
        """
        Register an event handler programmatically.

        Args:
            event_type: The event type to handle
            handler: The handler function
        """
        self._handlers[event_type].append(handler)

    def unregister_handler(self, event_type: str, handler: EventHandler) -> None:
        """
        Remove an event handler.

        Args:
            event_type: The event type
            handler: The handler to remove
        """
        if event_type in self._handlers:
            self._handlers[event_type] = [h for h in self._handlers[event_type] if h != handler]

    def get_handlers(self, event_type: str) -> list[EventHandler]:
        """
        Get all handlers for an event type.

        Args:
            event_type: The event type

        Returns:
            List of handlers
        """
        return list(self._handlers.get(event_type, []))

    def register_callback(self, callback_id: str, func: Callable[..., Any]) -> None:
        """
        Register a callback function.

        Args:
            callback_id: Unique identifier for the callback
            func: The callback function
        """
        self._callbacks[callback_id] = func

    def get_callback(self, callback_id: str) -> Callable[..., Any] | None:
        """
        Get a registered callback.

        Args:
            callback_id: The callback ID

        Returns:
            The callback function or None
        """
        return self._callbacks.get(callback_id)

    def add_middleware(self, middleware: Callable[..., Awaitable[Any]]) -> None:
        """
        Add middleware that runs before event handlers.

        Middleware signature: async def middleware(ctx, event, next) -> Any

        Args:
            middleware: The middleware function
        """
        self._middleware.append(middleware)

    async def emit(
        self,
        event_type: str,
        data: dict[str, Any] | None = None,
        ctx: "Context | None" = None,
    ) -> list[Any]:
        """
        Emit an event to all registered handlers.

        Args:
            event_type: The type of event
            data: Event data
            ctx: Request context

        Returns:
            List of results from all handlers
        """
        event = Event(type=event_type, data=data or {})
        handlers = self._handlers.get(event_type, [])

        if not handlers:
            logger.debug(f"No handlers for event: {event_type}")
            return []

        results = []
        for handler in handlers:
            try:
                # Run through middleware chain
                result = await self._run_with_middleware(ctx, event, handler)
                results.append(result)
            except Exception as e:
                logger.error(f"Error in handler for {event_type}: {e}")
                raise

        return results

    async def invoke_callback(
        self,
        callback_id: str,
        ctx: "Context",
        event_data: dict[str, Any],
    ) -> Any:
        """
        Invoke a registered callback.

        Args:
            callback_id: The callback ID
            ctx: Request context
            event_data: Data from the frontend event

        Returns:
            Result from the callback
        """
        callback = self._callbacks.get(callback_id)
        if callback is None:
            logger.warning(f"Callback not found: {callback_id}")
            return None

        # Extract bound args and call args
        bound_args = event_data.get("boundArgs", {})
        call_args = event_data.get("data", {})

        # Merge args (call_args override bound_args)
        merged_args = {**bound_args, **call_args}

        # Set event_data on context so callbacks can access it via ctx.event_data
        if hasattr(ctx, "set_event_data"):
            ctx.set_event_data(merged_args)

        # Set prop_store on context so callbacks can access stored values
        prop_store = event_data.get("propStore", {})
        if hasattr(ctx, "set_prop_store"):
            ctx.set_prop_store(prop_store)

        try:
            if asyncio.iscoroutinefunction(callback):
                return await callback(ctx, **merged_args)
            else:
                return callback(ctx, **merged_args)
        except Exception as e:
            logger.error(f"Error invoking callback {callback_id}: {e}")
            raise

    async def _run_with_middleware(
        self,
        ctx: "Context | None",
        event: Event,
        handler: EventHandler,
    ) -> Any:
        """
        Run handler with middleware chain.

        Args:
            ctx: Request context
            event: The event
            handler: The event handler

        Returns:
            Result from the handler
        """
        if not self._middleware:
            return await handler(ctx, event)

        # Build middleware chain
        async def run_handler(c: "Context | None", e: Event) -> Any:
            return await handler(c, e)

        chain = run_handler
        for middleware in reversed(self._middleware):
            chain = self._wrap_middleware(middleware, chain)

        return await chain(ctx, event)

    def _wrap_middleware(
        self,
        middleware: Callable[..., Awaitable[Any]],
        next_handler: Callable[..., Awaitable[Any]],
    ) -> Callable[..., Awaitable[Any]]:
        """
        Wrap a middleware function.

        Args:
            middleware: The middleware function
            next_handler: The next handler in the chain

        Returns:
            Wrapped function
        """

        async def wrapped(ctx: "Context | None", event: Event) -> Any:
            return await middleware(ctx, event, next_handler)

        return wrapped
