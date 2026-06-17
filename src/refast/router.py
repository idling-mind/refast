"""FastAPI router integration for Refast."""

import asyncio
import inspect
import logging
import re
import unicodedata
import urllib.parse
from collections.abc import Callable
from pathlib import Path
from typing import TYPE_CHECKING, Any

from fastapi import (
    APIRouter,
    File,
    HTTPException,
    Request,
    UploadFile,
    WebSocket,
    WebSocketDisconnect,
)
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, Response

from refast.assets import (
    STATIC_DIR,
    render_html_shell,
)
from refast.assets import (
    UNSAFE_CONTENT_TYPES as _UNSAFE_CONTENT_TYPES,
)
from refast.models.messages import client_message_adapter

if TYPE_CHECKING:
    from refast.app import RefastApp
    from refast.context import Context
    from refast.models.messages import (
        CallbackMessage,
        EventMessage,
        NavigateMessage,
        StoreInitMessage,
    )


logger = logging.getLogger(__name__)


# UUID format for validating file IDs received from URLs.
_UUID_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$",
    re.IGNORECASE,
)


def _parse_url(raw_path: str) -> tuple[str, dict[str, str], str]:
    """Split a raw URL path (possibly with a query string) into components.

    Returns:
        ``(pathname, query_params, query_string)`` where *pathname* has trailing
        slashes stripped, *query_params* is a ``dict[str, str]`` (last value
        wins for duplicate keys), and *query_string* is the raw query fragment
        without the leading ``?``.
    """
    parsed = urllib.parse.urlparse(raw_path)
    pathname = parsed.path if parsed.path else "/"
    if pathname != "/" and pathname.endswith("/"):
        pathname = pathname.rstrip("/")
    qs = parsed.query
    query_params: dict[str, str] = (
        {k: v[-1] for k, v in urllib.parse.parse_qs(qs).items()} if qs else {}
    )
    return pathname, query_params, qs


def _filter_callback_kwargs(
    sig: inspect.Signature,
    event_data_raw: dict[str, Any],
    callback_data: dict[str, Any],
) -> dict[str, Any]:
    """Build the keyword-argument dict to pass to a callback.

    Merges *event_data_raw* (DOM event fields) and *callback_data* (bound args /
    prop-store values), then filters down to only the parameters the callback
    actually declares — unless the callback accepts ``**kwargs``, in which case
    everything is forwarded.

    ``ctx`` is always excluded because the router passes it as the first
    positional argument.
    """
    params = sig.parameters
    has_var_keyword = any(p.kind == inspect.Parameter.VAR_KEYWORD for p in params.values())
    if has_var_keyword:
        return {**event_data_raw, **callback_data}
    combined = {**event_data_raw, **callback_data}
    return {k: v for k, v in combined.items() if k in params and k != "ctx"}


class RefastRouter:
    """
    FastAPI router that serves Refast pages.

    This router provides:
    - GET endpoints for each registered page
    - WebSocket endpoint for real-time updates
    - Static file serving for the React client
    """

    def __init__(self, app: "RefastApp"):
        self.app = app
        self.api_router = APIRouter()
        # Track contexts per WebSocket connection to preserve state
        self._websocket_contexts: dict[WebSocket, Context] = {}
        # Dispatch table: message type → handler coroutine method
        self._message_dispatch = {
            "callback": self._on_callback,
            "store_init": self._on_store_init,
            "navigate": self._on_navigate,
            "event": self._on_event,
        }
        self._setup_routes()

    def _setup_routes(self) -> None:
        """Set up all routes."""
        # WebSocket endpoint
        self.api_router.add_api_websocket_route(
            "/ws",
            self._websocket_handler,
        )

        # API endpoint for fetching page component tree (used for refresh)
        self.api_router.add_api_route(
            "/api/page",
            self._api_page_handler,
            methods=["GET"],
        )

        # Extension static file serving (must be before general static route)
        self.api_router.add_api_route(
            "/static/ext/{extension_name}/{filename:path}",
            self._extension_static_handler,
            methods=["GET"],
        )

        # Static file serving for Refast client
        self.api_router.add_api_route(
            "/static/{filename:path}",
            self._static_handler,
            methods=["GET"],
        )

        # File upload endpoint
        self.api_router.add_api_route(
            "/api/upload",
            self._upload_handler,
            methods=["POST"],
        )

        # File serving endpoint (used for create_file_url results)
        self.api_router.add_api_route(
            "/api/file/{file_id}",
            self._file_handler,
            methods=["GET"],
        )

        # Page routes are added dynamically
        self.api_router.add_api_route(
            "/{path:path}",
            self._page_handler,
            methods=["GET"],
            response_class=HTMLResponse,
        )

    async def _static_handler(self, request: Request, filename: str) -> Response:
        """Serve static files, with support for pre-compressed variants."""
        file_path = STATIC_DIR / filename

        # Prevent path traversal: resolved path must stay inside STATIC_DIR.
        try:
            file_path.resolve().relative_to(STATIC_DIR.resolve())
        except ValueError:
            return HTMLResponse(content="Not Found", status_code=404)

        if not file_path.exists() or not file_path.is_file():
            return HTMLResponse(content="Not Found", status_code=404)

        # Determine content type
        content_type = "application/octet-stream"
        suffix = file_path.suffix.lower()
        if suffix == ".js":
            content_type = "application/javascript"
        elif suffix == ".css":
            content_type = "text/css"
        elif suffix == ".html":
            content_type = "text/html"
        elif suffix == ".json":
            content_type = "application/json"
        elif suffix == ".svg":
            content_type = "image/svg+xml"
        elif suffix in (".png", ".jpg", ".jpeg", ".gif", ".webp"):
            content_type = f"image/{suffix[1:]}"

        # Try pre-compressed variant if the browser supports it
        accept_encoding = request.headers.get("accept-encoding", "")
        if suffix in (".js", ".css", ".json", ".svg", ".html"):
            if "br" in accept_encoding:
                br_path = file_path.with_suffix(file_path.suffix + ".br")
                if br_path.is_file():
                    return Response(
                        content=br_path.read_bytes(),
                        media_type=content_type,
                        headers={
                            "Content-Encoding": "br",
                            "Vary": "Accept-Encoding",
                        },
                    )
            if "gzip" in accept_encoding:
                gz_path = file_path.with_suffix(file_path.suffix + ".gz")
                if gz_path.is_file():
                    return Response(
                        content=gz_path.read_bytes(),
                        media_type=content_type,
                        headers={
                            "Content-Encoding": "gzip",
                            "Vary": "Accept-Encoding",
                        },
                    )

        return FileResponse(file_path, media_type=content_type)

    async def _extension_static_handler(self, extension_name: str, filename: str) -> FileResponse:
        """Serve static files from extensions."""
        extension = self.app.get_extension(extension_name)

        if extension is None:
            return HTMLResponse(content=f"Extension not found: {extension_name}", status_code=404)

        file_path = extension.get_static_file_path(filename)

        if file_path is None:
            return HTMLResponse(content=f"File not found: {filename}", status_code=404)

        # Determine content type
        content_type = "application/octet-stream"
        suffix = file_path.suffix.lower()
        if suffix == ".js":
            content_type = "application/javascript"
        elif suffix == ".css":
            content_type = "text/css"
        elif suffix == ".html":
            content_type = "text/html"
        elif suffix == ".json":
            content_type = "application/json"
        elif suffix == ".svg":
            content_type = "image/svg+xml"
        elif suffix in (".png", ".jpg", ".jpeg", ".gif", ".webp"):
            content_type = f"image/{suffix[1:]}"

        return FileResponse(file_path, media_type=content_type)

    async def _upload_handler(
        self,
        request: Request,
        files: list[UploadFile] = File(...),
    ) -> JSONResponse:
        """Handle multipart file uploads.

        Accepts one or more files via ``multipart/form-data`` under the field
        name ``files``.  Each file is stored in the app's :attr:`file_store`
        and its metadata is returned in the response.

        Returns:
            JSON ``{"files": [{id, name, size, content_type}]}``

        Status codes:
            * ``400`` – no files supplied
            * ``413`` – a file exceeds the store's ``max_size_bytes``
        """
        if not files:
            return JSONResponse(
                content={"error": "No files provided"},
                status_code=400,
            )

        max_files = self.app.max_upload_files
        if len(files) > max_files:
            return JSONResponse(
                content={"error": f"Too many files: maximum {max_files} per request"},
                status_code=400,
            )

        results = []
        store = self.app.file_store
        total_bytes = 0

        for upload in files:
            data = await upload.read()

            # Accumulate total upload size to prevent batch-level DoS.
            total_bytes += len(data)
            max_total = self.app.max_upload_size
            if max_total is not None and total_bytes > max_total:
                return JSONResponse(
                    content={"error": "Total upload size exceeds the allowed limit"},
                    status_code=413,
                )

            # Sanitize filename: take only the basename, remove control chars
            # and path separators so it is safe for Content-Disposition headers
            # and log output.
            raw_name = upload.filename or "upload"
            # Strip directory components first, then strip control / dangerous chars.
            sanitized = Path(raw_name).name
            sanitized = "".join(
                c
                for c in sanitized
                if unicodedata.category(c)[0] != "C" and c not in ("/", "\\", "\0")
            ).strip(" .")
            filename = sanitized or "upload"

            # Sanitize content type: never trust the client for active-content
            # MIME types that browsers can execute.
            _raw_ct_full = upload.content_type or "application/octet-stream"
            raw_ct = _raw_ct_full.split(";")[0].strip().lower()
            content_type = (
                "application/octet-stream" if raw_ct in _UNSAFE_CONTENT_TYPES else _raw_ct_full
            )

            try:
                info = await store.store_file(
                    data, filename, content_type, inline=False, user_upload=True
                )
            except ValueError as exc:
                return JSONResponse(
                    content={"error": str(exc), "file": filename},
                    status_code=413,
                )

            results.append(info.to_dict())

        return JSONResponse(content={"files": results})

    async def _file_handler(self, file_id: str) -> Response:
        """Serve a stored file by ID.

        Returns ``404`` if the file does not exist or has expired.
        The ``Content-Disposition`` header is set to ``inline`` or
        ``attachment`` according to how the file was stored.
        """
        # Validate file_id format (defense-in-depth; store checks also guard this).
        if not _UUID_RE.match(file_id):
            return JSONResponse(content={"error": "File not found or expired"}, status_code=404)

        store = self.app.file_store
        info = await store.get_file_info(file_id)
        if info is None:
            return JSONResponse(content={"error": "File not found or expired"}, status_code=404)

        data = await store.get_file(file_id)
        if data is None:
            return JSONResponse(content={"error": "File not found or expired"}, status_code=404)

        # Sanitize content type: remap active-content MIME types to a safe
        # binary type so browsers cannot execute uploaded payloads as scripts.
        # Only apply to user-uploaded files — server-generated files (stored
        # via ctx.create_file_url) are developer-controlled and served as-is.
        serve_ct = info.content_type
        if info.user_upload and serve_ct.split(";")[0].strip().lower() in _UNSAFE_CONTENT_TYPES:
            serve_ct = "application/octet-stream"

        # Build Content-Disposition with both the legacy ASCII-safe filename
        # (for older clients) and the RFC 5987 percent-encoded filename* parameter.
        disposition = "inline" if info.inline else "attachment"
        ascii_name = info.name.encode("ascii", errors="replace").decode().replace('"', "'")
        encoded_name = urllib.parse.quote(info.name, safe="")
        content_disposition = (
            f"{disposition}; filename=\"{ascii_name}\"; filename*=UTF-8''{encoded_name}"
        )

        return Response(
            content=data,
            media_type=serve_ct,
            headers={
                "Content-Disposition": content_disposition,
                "Content-Length": str(len(data)),
                "Cache-Control": "private, no-store",
                # Belt-and-suspenders: even though SecurityMiddleware adds this
                # globally, add it here too for deployments that skip the middleware.
                "X-Content-Type-Options": "nosniff",
            },
        )

    async def _page_handler(self, request: Request, path: str = "") -> HTMLResponse:
        """Handle page requests."""
        from refast.context import Context

        # Normalize path
        page_path = f"/{path}" if not path.startswith("/") else path
        if page_path != "/" and page_path.endswith("/"):
            page_path = page_path.rstrip("/")

        # Find the page (supports exact and parameterised routes)
        page_func, _path_params = self.app.match_route(page_path)
        if page_func is None:
            page_func = self.app._pages.get("/")  # Fallback to index

        if page_func is None:
            return HTMLResponse(content="<h1>404 - Page Not Found</h1>", status_code=404)

        # Do NOT call page_func here — components are created (and random IDs
        # assigned) only after the WebSocket connects via the store_init /
        # page_render flow.  Calling it twice caused a visible blink because
        # the initial tree (with one set of IDs) was immediately replaced by
        # the post-WebSocket tree (with a fresh set of IDs).
        ctx = Context(request=request, app=self.app)
        ctx._query_params = dict(request.query_params)
        ctx._query_string = str(request.url.query)
        ctx._path_params = _path_params
        html = self._render_html_shell(None, ctx)
        return HTMLResponse(content=html)

    async def _execute_page_func(
        self, page_func: Callable[..., Any], ctx: "Context", page_path: str
    ) -> Any:
        """Invoke a page function and reject unsupported return values."""
        component = page_func(ctx)
        if inspect.isawaitable(component):
            component = await component
        if component is None:
            func_name = getattr(page_func, "__name__", "<anonymous>")
            raise ValueError(
                f"Page function '{func_name}' for path '{page_path}' returned None. "
                "Page functions must return a component instance."
            )
        return component

    async def _api_page_handler(self, request: Request) -> JSONResponse:
        """Handle API requests for page component tree (used for refresh)."""
        from refast.context import Context

        # Get the referer header to determine which page to render
        referer = request.headers.get("referer", "/")

        # Extract path from referer URL
        from urllib.parse import urlparse

        parsed = urlparse(referer)
        page_path = parsed.path if parsed.path else "/"

        # Normalize path
        if page_path != "/" and page_path.endswith("/"):
            page_path = page_path.rstrip("/")

        # Find the page (supports exact and parameterised routes)
        page_func, path_params = self.app.match_route(page_path)
        if page_func is None:
            page_func = self.app._pages.get("/")  # Fallback to index

        if page_func is None:
            return JSONResponse(content={"error": "Page not found"}, status_code=404)

        # Create context and render page
        ctx = Context(request=request, app=self.app)
        ctx._path_params = path_params
        # Propagate query params from the referer URL's query string
        referer_qs = parsed.query
        ctx._query_string = referer_qs
        ctx._query_params = (
            {k: v[-1] for k, v in urllib.parse.parse_qs(referer_qs).items()} if referer_qs else {}
        )
        component = await self._execute_page_func(page_func, ctx, page_path)

        # Return component tree as JSON
        component_data = component.render() if hasattr(component, "render") else {}
        return JSONResponse(content=component_data)

    @property
    def active_contexts(self) -> list["Context"]:
        """Get all active WebSocket contexts."""
        return list(self._websocket_contexts.values())

    async def _websocket_handler(self, websocket: WebSocket) -> None:
        """Handle WebSocket connections for real-time updates."""
        await websocket.accept()

        # Create a single context for this WebSocket connection
        # This preserves state across all callback invocations
        from pydantic import ValidationError

        from refast.context import Context

        ctx = Context(websocket=websocket, app=self.app)
        self._websocket_contexts[websocket] = ctx

        try:
            while True:
                data = await websocket.receive_json()
                try:
                    message = client_message_adapter.validate_python(data)
                except ValidationError as exc:
                    logger.warning(f"WebSocket message validation failed: {exc}")
                    try:
                        await websocket.send_json(
                            {
                                "type": "validation_error",
                                "details": exc.errors(include_url=False),
                            }
                        )
                    except Exception as send_err:
                        logger.error(f"Failed to send validation error to client: {send_err}")
                    continue

                message_type = message.type

                # Handle store_sync immediately (it's a response to resync_store)
                # This must happen in the main loop to avoid deadlock when
                # a callback is waiting for sync response
                if message_type == "store_sync":
                    store_data = message.data
                    ctx._load_store_from_browser(store_data)
                    ctx._resolve_store_sync()
                elif message_type == "callback":
                    # Run callbacks in a separate task so the main loop can
                    # continue receiving messages (needed for store.sync())
                    asyncio.create_task(self._handle_websocket_message(websocket, message))
                else:
                    # Process other messages normally
                    await self._handle_websocket_message(websocket, message)
        except WebSocketDisconnect:
            # Clean up context when WebSocket disconnects
            self._websocket_contexts.pop(websocket, None)

    async def _handle_websocket_message(self, websocket: WebSocket, message: Any) -> None:
        """Dispatch an incoming WebSocket message to the appropriate handler."""
        message_type = message.type

        # Get the persistent context for this WebSocket connection
        ctx = self._websocket_contexts.get(websocket)
        if ctx is None:
            # Fallback: create a new context if not found (shouldn't happen)
            from refast.context import Context

            ctx = Context(websocket=websocket, app=self.app)
            self._websocket_contexts[websocket] = ctx

        handler = self._message_dispatch.get(message_type)
        if handler is not None:
            try:
                await handler(ctx, websocket, message)
            except HTTPException as exc:
                if self.app.debug:
                    try:
                        await websocket.send_json(
                            {
                                "type": "debug_event",
                                "event": {
                                    "type": "Python HTTP Exception",
                                    "message": f"HTTP {exc.status_code}: {exc.detail}",
                                    "details": {
                                        "messageType": message_type,
                                        "statusCode": exc.status_code,
                                        "detail": exc.detail,
                                        "messageData": getattr(
                                            message, "model_dump", lambda: str(message)
                                        )(),
                                    },
                                },
                            }
                        )
                    except Exception as send_err:
                        logger.error(f"Failed to send debug error message: {send_err}")
                if message_type in ("store_init", "navigate"):
                    from refast.components import Column, Heading, Icon, Text

                    icon_name = "alert-triangle" if 400 <= exc.status_code < 500 else "alert-circle"
                    error_component = Column(
                        class_name=(
                            "p-8 h-screen flex flex-col items-center justify-center space-y-4"
                        ),
                        align="center",
                        justify="center",
                        children=[
                            Icon(icon_name, size=48, color="#ef4444"),
                            Heading(
                                f"Error {exc.status_code}",
                                class_name="text-4xl font-bold text-destructive",
                            ),
                            Text(
                                exc.detail or "An error occurred",
                                class_name="text-lg text-muted-foreground",
                            ),
                        ],
                    )
                    component_data = (
                        error_component.render() if hasattr(error_component, "render") else {}
                    )
                    await websocket.send_json({"type": "page_render", "component": component_data})
                elif message_type in ("callback", "event"):
                    await ctx.show_toast(
                        message=f"Error {exc.status_code}",
                        description=str(exc.detail),
                        variant="destructive",
                    )
            except Exception as exc:
                logger.error(
                    f"Unexpected error handling message {message_type}: {exc}", exc_info=True
                )
                if self.app.debug:
                    import traceback

                    tb = traceback.format_exc()
                    try:
                        await websocket.send_json(
                            {
                                "type": "debug_event",
                                "event": {
                                    "type": "Python Callback Exception",
                                    "message": f"{type(exc).__name__}: {exc}",
                                    "details": {
                                        "messageType": message_type,
                                        "exception": type(exc).__name__,
                                        "traceback": tb,
                                        "messageData": getattr(
                                            message, "model_dump", lambda: str(message)
                                        )(),
                                    },
                                },
                            }
                        )
                    except Exception as send_err:
                        logger.error(f"Failed to send debug error message: {send_err}")
                if message_type in ("store_init", "navigate"):
                    from refast.components import Column, Heading, Icon, Text

                    error_component = Column(
                        class_name=(
                            "p-8 h-screen flex flex-col items-center justify-center space-y-4"
                        ),
                        align="center",
                        justify="center",
                        children=[
                            Icon("alert-circle", size=48, color="#ef4444"),
                            Heading("Error 500", class_name="text-4xl font-bold text-destructive"),
                            Text(
                                "Internal Server Error", class_name="text-lg text-muted-foreground"
                            ),
                        ],
                    )
                    component_data = (
                        error_component.render() if hasattr(error_component, "render") else {}
                    )
                    await websocket.send_json({"type": "page_render", "component": component_data})
                elif message_type in ("callback", "event"):
                    await ctx.show_toast(message="Internal Server Error", variant="destructive")

    async def _on_callback(
        self, ctx: "Context", websocket: WebSocket, message: "CallbackMessage"
    ) -> None:
        """Handle a ``callback`` message: invoke a registered Python callback."""
        callback_id = message.callback_id
        callback_data = message.data
        event_data_raw = message.event_data

        callback = ctx.get_callback(callback_id)
        if callback:
            ctx.set_event_data(event_data_raw)
            kwargs = _filter_callback_kwargs(
                inspect.signature(callback), event_data_raw, callback_data
            )
            await callback(ctx, **kwargs)
            await ctx.sync_store()
        elif self.app.debug:
            await websocket.send_json(
                {
                    "type": "debug_event",
                    "event": {
                        "type": "Missing Python Callback",
                        "message": f"Callback ID '{callback_id}' is not registered on the backend.",
                        "details": {
                            "callbackId": callback_id,
                            "data": callback_data,
                            "eventData": event_data_raw,
                        },
                    },
                }
            )

    async def _on_store_init(
        self, ctx: "Context", websocket: WebSocket, message: "StoreInitMessage"
    ) -> None:
        """Handle a ``store_init`` message: load browser storage then render the page."""
        store_data = message.data
        ctx._load_store_from_browser(store_data)

        raw_path = message.path
        pathname, query_params, query_string = _parse_url(raw_path)
        ctx._current_path = pathname
        ctx._query_params = query_params
        ctx._query_string = query_string

        page_func, path_params = self.app.match_route(pathname)
        ctx._path_params = path_params
        if page_func is None:
            page_func = self.app._pages.get("/")
        if page_func is not None:
            ctx.clear_callbacks()
            component = await self._execute_page_func(page_func, ctx, pathname)
            component_data = component.render() if hasattr(component, "render") else {}
            await websocket.send_json({"type": "page_render", "component": component_data})

        await websocket.send_json({"type": "store_ready"})

    async def _on_navigate(
        self, ctx: "Context", websocket: WebSocket, message: "NavigateMessage"
    ) -> None:
        """Handle a ``navigate`` message: render the page for the requested path."""
        raw_path = message.path
        pathname, query_params, query_string = _parse_url(raw_path)
        ctx._current_path = pathname
        ctx._query_params = query_params
        ctx._query_string = query_string

        page_func, path_params = self.app.match_route(pathname)
        ctx._path_params = path_params
        if page_func is None:
            page_func = self.app._pages.get("/")
        if page_func is not None:
            ctx.clear_callbacks()
            component = await self._execute_page_func(page_func, ctx, pathname)
            component_data = component.render() if hasattr(component, "render") else {}
            await websocket.send_json({"type": "page_render", "component": component_data})

    async def _on_event(
        self, ctx: "Context", websocket: WebSocket, message: "EventMessage"
    ) -> None:
        """Handle a custom ``event`` message: invoke the registered event handler."""
        event_type = message.event_type
        handler = self.app._event_handlers.get(event_type)
        if handler:
            from refast.events.types import Event

            event = Event(type=event_type, data=message.data)
            await handler(ctx, event)

    def _render_html_shell(self, component, ctx):
        """Render the HTML shell. Delegates to render_html_shell(self.app)."""
        return render_html_shell(self.app)
