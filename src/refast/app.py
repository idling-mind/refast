"""Main RefastApp class."""

import logging
from collections.abc import Callable
from typing import TYPE_CHECKING, Any, TypeVar

from fastapi import APIRouter

from refast.router import RefastRouter

if TYPE_CHECKING:
    from refast.context import Context
    from refast.extensions import Extension

PageFunc = TypeVar("PageFunc", bound=Callable[..., Any])

logger = logging.getLogger(__name__)


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
        extensions: List of Extension instances to register
        auto_discover_extensions: Whether to auto-discover extensions via entry points
    """

    def __init__(
        self,
        title: str = "Refast App",
        theme: str | dict[str, Any] | None = None,
        secret_key: str | None = None,
        debug: bool = False,
        extensions: list["Extension"] | None = None,
        auto_discover_extensions: bool = True,
    ):
        self.title = title
        self.theme = theme
        self.secret_key = secret_key
        self.debug = debug

        self._pages: dict[str, Callable] = {}
        self._callbacks: dict[str, Callable] = {}
        self._event_handlers: dict[str, Callable] = {}
        self._router: RefastRouter | None = None
        self._extensions: dict[str, "Extension"] = {}

        # Auto-discover extensions via entry points
        if auto_discover_extensions:
            self._discover_extensions()

        # Register manually provided extensions
        if extensions:
            for ext in extensions:
                self.register_extension(ext)

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

    # Extension methods

    @property
    def extensions(self) -> dict[str, "Extension"]:
        """Get registered extensions."""
        return self._extensions.copy()

    def register_extension(self, extension: "Extension") -> None:
        """
        Register an extension with this app.

        Args:
            extension: The Extension instance to register.

        Raises:
            ValueError: If an extension with the same name is already registered.

        Example:
            ```python
            from refast_leaflet import LeafletExtension

            ui = RefastApp()
            ui.register_extension(LeafletExtension())
            ```
        """
        from refast.extensions import Extension

        if not isinstance(extension, Extension):
            raise TypeError(
                f"Expected Extension instance, got {type(extension).__name__}"
            )

        if extension.name in self._extensions:
            raise ValueError(
                f"Extension '{extension.name}' is already registered"
            )

        # Validate extension configuration
        errors = extension.validate()
        if errors and self.debug:
            for error in errors:
                logger.warning(f"Extension validation warning: {error}")

        # Register the extension
        self._extensions[extension.name] = extension

        # Call the extension's on_register hook
        extension.on_register(self)

        logger.debug(f"Registered extension: {extension.name} v{extension.version}")

    def _discover_extensions(self) -> None:
        """
        Discover and register extensions via Python entry points.

        Extensions can register themselves using the 'refast.extensions'
        entry point group in their pyproject.toml:

            [project.entry-points."refast.extensions"]
            my_extension = "my_package:MyExtension"
        """
        try:
            from importlib.metadata import entry_points
        except ImportError:
            # Python < 3.10 fallback
            from importlib_metadata import entry_points  # type: ignore

        try:
            # Python 3.10+ style
            eps = entry_points(group="refast.extensions")
        except TypeError:
            # Python 3.9 style
            all_eps = entry_points()
            eps = all_eps.get("refast.extensions", [])

        for ep in eps:
            try:
                extension_class = ep.load()
                extension = extension_class()
                self.register_extension(extension)
                logger.debug(f"Auto-discovered extension: {ep.name}")
            except Exception as e:
                logger.warning(
                    f"Failed to load extension '{ep.name}': {e}"
                )

    def get_extension(self, name: str) -> "Extension | None":
        """
        Get a registered extension by name.

        Args:
            name: The extension name.

        Returns:
            The Extension instance, or None if not found.
        """
        return self._extensions.get(name)

