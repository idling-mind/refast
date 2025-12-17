"""FastAPI router integration for Refast."""

from pathlib import Path
from typing import TYPE_CHECKING, Any

from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, FileResponse

if TYPE_CHECKING:
    from refast.app import RefastApp
    from refast.context import Context


# Get the static directory path
STATIC_DIR = Path(__file__).parent / "static"


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
        self._websocket_contexts: dict[WebSocket, "Context"] = {}
        self._setup_routes()

    def _setup_routes(self) -> None:
        """Set up all routes."""
        # WebSocket endpoint
        self.api_router.add_api_websocket_route(
            "/ws",
            self._websocket_handler,
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

    async def _static_handler(self, filename: str) -> FileResponse:
        """Serve static files."""
        file_path = STATIC_DIR / filename
        
        if not file_path.exists() or not file_path.is_file():
            # Return 404 for missing files
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
                # Process incoming events using the persistent context
                await self._handle_websocket_message(websocket, data)
        except WebSocketDisconnect:
            # Clean up context when WebSocket disconnects
            self._websocket_contexts.pop(websocket, None)

    async def _handle_websocket_message(
        self, websocket: WebSocket, data: dict[str, Any]
    ) -> None:
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

            callback = self.app.get_callback(callback_id)
            if callback:
                # Filter callback_data to only include parameters the callback accepts
                sig = inspect.signature(callback)
                params = sig.parameters
                
                # Check if callback accepts **kwargs
                has_var_keyword = any(
                    p.kind == inspect.Parameter.VAR_KEYWORD 
                    for p in params.values()
                )
                
                if has_var_keyword:
                    # Callback accepts **kwargs, pass all data
                    await callback(ctx, **callback_data)
                else:
                    # Filter to only accepted parameters (excluding 'ctx')
                    accepted_params = {
                        k: v for k, v in callback_data.items() 
                        if k in params and k != 'ctx'
                    }
                    await callback(ctx, **accepted_params)

        elif message_type == "event":
            event_type = data.get("eventType")
            handler = self.app._event_handlers.get(event_type)
            if handler:
                from refast.events.types import Event
                event = Event(type=event_type, data=data.get("data", {}))
                await handler(ctx, event)

    def _render_html_shell(self, component: Any, ctx: "Context") -> str:
        """Render the HTML shell with embedded component data."""
        import json

        component_data = component.render() if hasattr(component, "render") else {}
        component_json = json.dumps(component_data)
        
        # Check if React client assets are available
        client_js_path = STATIC_DIR / "refast-client.js"
        client_css_path = STATIC_DIR / "refast-client.css"
        has_client_js = client_js_path.exists()
        has_client_css = client_css_path.exists()
        
        # Include client assets if they exist
        client_css = '<link rel="stylesheet" href="/static/refast-client.css">' if has_client_css else ''
        client_script = '<script src="/static/refast-client.js"></script>' if has_client_js else ''

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{self.app.title}</title>
    {client_css}
    <script>
        window.__REFAST_INITIAL_DATA__ = {component_json};
    </script>
</head>
<body>
    <div id="refast-root"></div>
    {client_script}
</body>
</html>"""
