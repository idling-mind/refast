"""Main RefastApp class."""

from collections.abc import Callable
from typing import TYPE_CHECKING, Any, TypeVar

from fastapi import APIRouter

from refast.router import RefastRouter

if TYPE_CHECKING:
    from refast.context import Context

PageFunc = TypeVar("PageFunc", bound=Callable[..., Any])


class RefastApp:
    """
    Main Refast application class.

    Example:
        ```python
        from refast import RefastApp

        ui = RefastApp(title="My App")

        @ui.page("/")
        def home(ctx: Context):
            return Container(Text("Hello World"))

        # Mount to FastAPI
        app.include_router(ui.router, prefix="/ui")
        ```

    Args:
        title: Application title
        theme: Theme configuration (default or custom)
        secret_key: Secret key for session encryption
        debug: Enable debug mode
    """

    def __init__(
        self,
        title: str = "Refast App",
        theme: str | dict[str, Any] | None = None,
        secret_key: str | None = None,
        debug: bool = False,
    ):
        self.title = title
        self.theme = theme
        self.secret_key = secret_key
        self.debug = debug

        self._pages: dict[str, Callable] = {}
        self._callbacks: dict[str, Callable] = {}
        self._event_handlers: dict[str, Callable] = {}
        self._router: RefastRouter | None = None

    @property
    def router(self) -> APIRouter:
        """Get the FastAPI router for mounting."""
        if self._router is None:
            self._router = RefastRouter(self)
        return self._router.api_router

    @property
    def active_contexts(self) -> list["Context"]:
        """Get all active WebSocket contexts."""
        if self._router is None:
            return []
        return self._router.active_contexts

    @property
    def pages(self) -> dict[str, Callable]:
        """Get registered pages."""
        return self._pages.copy()

    def page(self, path: str) -> Callable[[PageFunc], PageFunc]:
        """
        Decorator to register a page.

        Args:
            path: URL path for the page

        Returns:
            Decorator function

        Example:
            ```python
            @ui.page("/dashboard")
            def dashboard(ctx: Context):
                return Container(...)
            ```
        """

        def decorator(func: PageFunc) -> PageFunc:
            self._pages[path] = func
            return func

        return decorator

    def on_event(self, event_type: str) -> Callable[[Callable], Callable]:
        """
        Decorator to register an event handler.

        Args:
            event_type: The event type to handle (e.g., "user:click")

        Returns:
            Decorator function
        """

        def decorator(func: Callable) -> Callable:
            self._event_handlers[event_type] = func
            return func

        return decorator

    def register_callback(self, callback_id: str, func: Callable) -> None:
        """Register a callback function."""
        self._callbacks[callback_id] = func

    def get_callback(self, callback_id: str) -> Callable | None:
        """Get a registered callback by ID."""
        return self._callbacks.get(callback_id)
