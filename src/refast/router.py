"""FastAPI router integration for Refast."""

import asyncio
import json as json_module
from pathlib import Path
from typing import TYPE_CHECKING, Any

from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse, Response

if TYPE_CHECKING:
    from refast.app import RefastApp
    from refast.context import Context


# Get the static directory path
STATIC_DIR = Path(__file__).parent / "static"

# All known lazy feature-chunk names (must match vite manualChunks keys)
ALL_FEATURE_CHUNKS = frozenset(
    {
        "charts",
        "markdown",
        "icons",
        "navigation",
        "overlay",
        "controls",
    }
)


def _load_manifest() -> dict[str, Any]:
    """Load the Vite build manifest from static/manifest.json.

    Returns an empty dict if the file doesn't exist (pre-built assets
    may not include a manifest in development).
    """
    manifest_path = STATIC_DIR / "manifest.json"
    if manifest_path.is_file():
        return json_module.loads(manifest_path.read_text(encoding="utf-8"))
    return {}


def _get_chunk_files(manifest: dict[str, Any], features: list[str] | None) -> list[str]:
    """Derive the list of JS chunk filenames to include from the manifest.

    Args:
        manifest: Parsed Vite manifest.json contents.
        features: ``None`` = load all chunks; otherwise only the listed
            feature chunks are included.

    Returns:
        List of JS filenames (relative to /static/) in load order.
        The entry chunk (``refast-client.js``) is always first.
    """
    if not manifest:
        # Fallback: no manifest, just return the entry file
        return ["refast-client.js"]

    # Collect all chunk filenames from the manifest
    chunk_files: list[str] = []
    for _key, entry in manifest.items():
        file = entry.get("file", "")
        if file and file.endswith(".js"):
            chunk_files.append(file)

    if not chunk_files:
        return ["refast-client.js"]

    # Determine which feature chunks to include
    if features is not None:
        allowed = set(features)
    else:
        allowed = set(ALL_FEATURE_CHUNKS)

    # Separate entry from feature chunks
    result: list[str] = []
    deferred: list[str] = []
    for f in chunk_files:
        if f == "refast-client.js":
            result.insert(0, f)
            continue
        # Check if this chunk belongs to a feature group
        # Chunk names look like: refast-charts-abc123.js
        chunk_feature = None
        for feat in ALL_FEATURE_CHUNKS:
            if f.startswith(f"refast-{feat}-"):
                chunk_feature = feat
                break

        if chunk_feature is None:
            # Shared / vendor chunk – always include
            deferred.append(f)
        elif chunk_feature in allowed:
            deferred.append(f)
        # else: excluded feature chunk – skip

    # Entry must come first; ensure it's present
    if "refast-client.js" not in result:
        result.insert(0, "refast-client.js")

    result.extend(deferred)
    return result


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

    async def _page_handler(self, request: Request, path: str = "") -> HTMLResponse:
        """Handle page requests."""
        from refast.context import Context

        # Normalize path
        page_path = f"/{path}" if not path.startswith("/") else path
        if page_path != "/" and page_path.endswith("/"):
            page_path = page_path.rstrip("/")

        # Find the page
        page_func = self.app._pages.get(page_path)
        if page_func is None:
            page_func = self.app._pages.get("/")  # Fallback to index

        if page_func is None:
            return HTMLResponse(content="<h1>404 - Page Not Found</h1>", status_code=404)

        # Create context and render page
        ctx = Context(request=request, app=self.app)
        component = page_func(ctx)

        # Render to HTML shell with component data
        html = self._render_html_shell(component, ctx)
        return HTMLResponse(content=html)

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

        # Find the page
        page_func = self.app._pages.get(page_path)
        if page_func is None:
            page_func = self.app._pages.get("/")  # Fallback to index

        if page_func is None:
            return JSONResponse(content={"error": "Page not found"}, status_code=404)

        # Create context and render page
        ctx = Context(request=request, app=self.app)
        component = page_func(ctx)

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
        from refast.context import Context

        ctx = Context(websocket=websocket, app=self.app)
        self._websocket_contexts[websocket] = ctx

        try:
            while True:
                data = await websocket.receive_json()
                message_type = data.get("type")

                # Handle store_sync immediately (it's a response to resync_store)
                # This must happen in the main loop to avoid deadlock when
                # a callback is waiting for sync response
                if message_type == "store_sync":
                    store_data = data.get("data", {})
                    ctx._load_store_from_browser(store_data)
                    ctx._resolve_store_sync()
                elif message_type == "callback":
                    # Run callbacks in a separate task so the main loop can
                    # continue receiving messages (needed for store.sync())
                    asyncio.create_task(self._handle_websocket_message(websocket, data))
                else:
                    # Process other messages normally
                    await self._handle_websocket_message(websocket, data)
        except WebSocketDisconnect:
            # Clean up context when WebSocket disconnects
            self._websocket_contexts.pop(websocket, None)

    async def _handle_websocket_message(self, websocket: WebSocket, data: dict[str, Any]) -> None:
        """Process incoming WebSocket messages."""
        import inspect

        message_type = data.get("type")

        # Get the persistent context for this WebSocket connection
        ctx = self._websocket_contexts.get(websocket)
        if ctx is None:
            # Fallback: create a new context if not found (shouldn't happen)
            from refast.context import Context

            ctx = Context(websocket=websocket, app=self.app)
            self._websocket_contexts[websocket] = ctx

        if message_type == "callback":
            callback_id = data.get("callbackId")
            callback_data = data.get("data", {})
            event_data_raw = data.get("eventData", {})

            callback = self.app.get_callback(callback_id)
            if callback:
                # Set raw DOM event data on context (accessible via ctx.event_data)
                ctx.set_event_data(event_data_raw)

                # Filter callback_data to only include parameters the callback accepts
                sig = inspect.signature(callback)
                params = sig.parameters

                # Check if callback accepts **kwargs
                has_var_keyword = any(
                    p.kind == inspect.Parameter.VAR_KEYWORD for p in params.values()
                )

                if has_var_keyword:
                    # Callback accepts **kwargs, pass all data
                    await callback(ctx, **callback_data)
                else:
                    # Filter to only accepted parameters (excluding 'ctx')
                    accepted_params = {
                        k: v for k, v in callback_data.items() if k in params and k != "ctx"
                    }
                    await callback(ctx, **accepted_params)

                # Sync any pending store updates after callback
                await ctx.sync_store()

        elif message_type == "store_init":
            # Browser is sending its current storage state on connect
            store_data = data.get("data", {})
            ctx._load_store_from_browser(store_data)

            # Get the page path from the data (sent by frontend)
            page_path = data.get("path", "/")

            # Find and render the page with the loaded store
            page_func = self.app._pages.get(page_path)
            if page_func is None:
                page_func = self.app._pages.get("/")  # Fallback to index

            if page_func is not None:
                component = page_func(ctx)
                component_data = component.render() if hasattr(component, "render") else {}

                # Send the rendered page via WebSocket
                await websocket.send_json(
                    {
                        "type": "page_render",
                        "component": component_data,
                    }
                )

            # Send acknowledgment so frontend knows store is ready
            await websocket.send_json({"type": "store_ready"})

        elif message_type == "navigate":
            # Client requesting page render for a new path
            # (e.g. browser back/forward via popstate)
            page_path = data.get("path", "/")
            if page_path != "/" and page_path.endswith("/"):
                page_path = page_path.rstrip("/")
            page_func = self.app._pages.get(page_path)
            if page_func is None:
                page_func = self.app._pages.get("/")  # Fallback to index
            if page_func is not None:
                component = page_func(ctx)
                component_data = component.render() if hasattr(component, "render") else {}
                await websocket.send_json(
                    {
                        "type": "page_render",
                        "component": component_data,
                    }
                )

        elif message_type == "event":
            event_type = data.get("eventType")
            handler = self.app._event_handlers.get(event_type)
            if handler:
                from refast.events.types import Event

                event = Event(type=event_type, data=data.get("data", {}))
                await handler(ctx, event)

    def _render_html_shell(self, component: Any, ctx: "Context") -> str:
        """Render the HTML shell with embedded component data.

        The shell uses ``<script type="module">`` for the ESM entry chunk
        and any additional feature chunks determined by the build manifest
        and the app's ``features`` configuration.

        Extension scripts are loaded *after* the core module fires
        ``refast:ready``, ensuring ``window.RefastClient`` is available.
        """
        import json

        component_data = component.render() if hasattr(component, "render") else {}
        component_json = json.dumps(component_data)

        # Check if React client CSS exists
        client_css_path = STATIC_DIR / "refast-client.css"
        has_client_css = client_css_path.exists()

        # Resolve chunk files from the build manifest
        manifest = _load_manifest()
        chunk_files = _get_chunk_files(manifest, self.app.features)

        # Build script tags — entry is type="module", chunks are modulepreload
        client_css = (
            '<link rel="stylesheet" href="/static/refast-client.css">' if has_client_css else ""
        )

        # The entry module + feature chunks
        script_tags: list[str] = []
        preload_tags: list[str] = []
        for f in chunk_files:
            path = f"/static/{f}"
            if f == "refast-client.js":
                script_tags.append(f'<script type="module" src="{path}"></script>')
            else:
                # Preload hints let the browser fetch chunks early
                preload_tags.append(f'<link rel="modulepreload" href="{path}">')

        scripts_html = "\n    ".join(script_tags)
        preloads_html = "\n    ".join(preload_tags)

        # Collect extension assets — loaded after refast:ready
        extension_styles = []
        extension_scripts_list = []
        for ext in self.app._extensions.values():
            extension_styles.extend(
                f'<link rel="stylesheet" href="{url}">' for url in ext.get_style_urls()
            )
            extension_scripts_list.extend(ext.get_script_urls())

        ext_styles_html = "\n    ".join(extension_styles)

        # Extensions are IIFE scripts that need window.RefastClient.
        # We inject them via a small inline module that waits for refast:ready.
        ext_loader_html = ""
        if extension_scripts_list:
            urls_json = json.dumps(extension_scripts_list)
            ext_loader_html = f"""<script type="module">
    function loadExtensions() {{
      {urls_json}.forEach(function(url) {{
        var s = document.createElement('script');
        s.src = url;
        document.body.appendChild(s);
      }});
    }}
    if (window.RefastClient) {{
      loadExtensions();
    }} else {{
      window.addEventListener('refast:ready', loadExtensions, {{ once: true }});
    }}
    </script>"""

        # --- Theme CSS variable overrides ---
        theme_style = ""
        if self.app.theme is not None:
            css_vars = self.app.theme.to_css_variables()
            if css_vars:
                theme_style = f"<style data-refast-theme>\n{css_vars}\n</style>"

        # --- Favicon ---
        favicon_tag = ""
        if self.app.favicon:
            favicon_tag = f'<link rel="icon" href="{self.app.favicon}">'

        # --- Extra <head> tags ---
        head_tags_html = "\n    ".join(self.app._head_tags) if self.app._head_tags else ""

        # --- Custom CSS (after extension CSS so user overrides win) ---
        custom_css_parts: list[str] = []
        for entry in self.app._custom_css:
            if entry.startswith("http") or entry.startswith("/"):
                custom_css_parts.append(f'<link rel="stylesheet" href="{entry}">')
            else:
                custom_css_parts.append(f"<style>{entry}</style>")
        custom_css_html = "\n    ".join(custom_css_parts)

        # --- Custom JS (after client + extension scripts so globals exist) ---
        custom_js_parts: list[str] = []
        for entry in self.app._custom_js:
            if entry.startswith("http") or entry.startswith("/"):
                custom_js_parts.append(f'<script src="{entry}"></script>')
            else:
                custom_js_parts.append(f"<script>{entry}</script>")
        custom_js_html = "\n    ".join(custom_js_parts)

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.app.title}</title>
    {favicon_tag}
    {client_css}
    {preloads_html}
    {theme_style}
    {ext_styles_html}
    {custom_css_html}
    {head_tags_html}
    <script>
        window.__REFAST_INITIAL_DATA__ = {component_json};
    </script>
</head>
<body>
    <div id="refast-root"></div>
    {scripts_html}
    {ext_loader_html}
    {custom_js_html}
</body>
</html>"""
