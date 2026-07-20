"""Event manager for routing events."""

import logging
import inspect
import typing
from collections import defaultdict
from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any
from pydantic import BaseModel

from refast.events.types import Event, EventHandler

if TYPE_CHECKING:
    from refast.app import RefastApp
    from refast.context import Context

logger = logging.getLogger(__name__)


def get_handler_event_payload_model(func: Callable[..., Any]) -> type[BaseModel] | None:
    """
    Inspect a handler function to see if its event parameter is annotated as Event[T],
    where T is a subclass of Pydantic's BaseModel.
    """
    try:
        hints = typing.get_type_hints(func)
    except Exception:
        hints = {}
        # Fallback to direct parameter annotations if get_type_hints fails
        try:
            sig = inspect.signature(func)
            for name, param in sig.parameters.items():
                if param.annotation is not inspect.Parameter.empty:
                    hints[name] = param.annotation
        except Exception:
            pass

    from refast.events.types import Event

    for hint in hints.values():
        origin = typing.get_origin(hint)
        # Handle Event[T]
        if origin is Event:
            args = typing.get_args(hint)
            if args:
                arg = args[0]
                try:
                    if isinstance(arg, type) and issubclass(arg, BaseModel):
                        return arg
                except TypeError:
                    pass
    return None


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
        self._middleware: list[Callable[..., Any]] = []
        self._event_error_handlers: dict[Callable[..., Any], Callable[..., Any]] = {}

    def on(
        self,
        event_type: str,
        on_error: Callable[..., Any] | None = None,
    ) -> Callable[[EventHandler], EventHandler]:
        """
        Decorator to register an event handler.

        Args:
            event_type: The event type to handle
            on_error: Optional error handler function called if validation
                or execution fails. Signature: async def handle_error(ctx, error, event)

        Returns:
            Decorator function
        """

        def decorator(func: EventHandler) -> EventHandler:
            self._handlers[event_type].append(func)
            if on_error is not None:
                self._event_error_handlers[func] = on_error
            return func

        return decorator

    def register_handler(
        self,
        event_type: str,
        handler: EventHandler,
        on_error: Callable[..., Any] | None = None,
    ) -> None:
        """
        Register an event handler programmatically.

        Args:
            event_type: The event type to handle
            handler: The handler function
            on_error: Optional error handler function called if validation
                or execution fails.
        """
        self._handlers[event_type].append(handler)
        if on_error is not None:
            self._event_error_handlers[handler] = on_error

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
        model_class = get_handler_event_payload_model(handler)

        async def execute_handler(c: "Context | None", e: Event) -> Any:
            try:
                if model_class is not None:
                    from dataclasses import replace
                    validated_data = model_class.model_validate(e.data)
                    e = replace(e, data=validated_data)
                return await handler(c, e)
            except Exception as exc:
                error_handler = self._event_error_handlers.get(handler)
                if error_handler is not None:
                    return await error_handler(c, exc, event=e)
                raise

        if not self._middleware:
            return await execute_handler(ctx, event)

        # Build middleware chain
        chain = execute_handler
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
