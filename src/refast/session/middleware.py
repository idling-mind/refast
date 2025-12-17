"""Session middleware for automatic session handling."""

from collections.abc import Callable
from typing import TYPE_CHECKING

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from refast.session.session import Session, SessionData
from refast.session.stores.base import SessionStore
from refast.session.stores.memory import MemorySessionStore

if TYPE_CHECKING:
    from fastapi import FastAPI


class SessionMiddleware(BaseHTTPMiddleware):
    """
    Middleware that handles session lifecycle.

    - Loads session from cookie
    - Attaches session to request state
    - Saves session after response
    - Sets session cookie

    Example:
        ```python
        app = FastAPI()

        store = MemorySessionStore()
        app.add_middleware(
            SessionMiddleware,
            store=store,
            cookie_name="refast_session",
            secret_key="your-secret-key",
        )

        @app.get("/")
        async def home(request: Request):
            session = request.state.session
            session.set("visits", session.get("visits", 0) + 1)
            return {"visits": session.get("visits")}
        ```

    Attributes:
        store: The session store backend
        cookie_name: Name of the session cookie
        cookie_max_age: Cookie max age in seconds
    """

    def __init__(
        self,
        app: "FastAPI",
        store: SessionStore | None = None,
        cookie_name: str = "refast_session",
        cookie_max_age: int = 3600,
        cookie_path: str = "/",
        cookie_domain: str | None = None,
        cookie_secure: bool = False,
        cookie_httponly: bool = True,
        cookie_samesite: str = "lax",
        secret_key: str | None = None,
    ):
        """
        Initialize the session middleware.

        Args:
            app: The FastAPI application
            store: Session store backend (defaults to MemorySessionStore)
            cookie_name: Name of the session cookie
            cookie_max_age: Cookie max age in seconds
            cookie_path: Cookie path
            cookie_domain: Cookie domain
            cookie_secure: Whether cookie requires HTTPS
            cookie_httponly: Whether cookie is HTTP-only
            cookie_samesite: Cookie SameSite policy
            secret_key: Secret key for signing (future use)
        """
        super().__init__(app)
        self.store = store or MemorySessionStore()
        self.cookie_name = cookie_name
        self.cookie_max_age = cookie_max_age
        self.cookie_path = cookie_path
        self.cookie_domain = cookie_domain
        self.cookie_secure = cookie_secure
        self.cookie_httponly = cookie_httponly
        self.cookie_samesite = cookie_samesite
        self.secret_key = secret_key

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Response],
    ) -> Response:
        """
        Process request with session handling.

        Args:
            request: The incoming request
            call_next: The next handler in the chain

        Returns:
            The response with session cookie set
        """
        # Get session ID from cookie
        session_id = request.cookies.get(self.cookie_name)

        # Load or create session
        session = await self._load_session(session_id)

        # Attach to request
        request.state.session = session

        # Process request
        response = await call_next(request)

        # Save session if modified
        if session.is_modified:
            await session.save()

        # Set cookie
        response.set_cookie(
            key=self.cookie_name,
            value=session.id,
            max_age=self.cookie_max_age,
            path=self.cookie_path,
            domain=self.cookie_domain,
            secure=self.cookie_secure,
            httponly=self.cookie_httponly,
            samesite=self.cookie_samesite,
        )

        return response

    async def _load_session(self, session_id: str | None) -> Session:
        """
        Load session from store or create new one.

        Args:
            session_id: The session ID from cookie

        Returns:
            The loaded or new session
        """
        if session_id:
            data = await self.store.get(session_id)
            if data:
                session_data = SessionData.from_dict(data)
                if not session_data.is_expired():
                    return Session(session_data, self.store)

        # Create new session
        session_data = SessionData()
        return Session(session_data, self.store)


def get_session(request: Request) -> Session:
    """
    Dependency to get session from request.

    Example:
        ```python
        from fastapi import Depends

        @app.get("/")
        async def home(session: Session = Depends(get_session)):
            return {"user": session.get("user")}
        ```

    Args:
        request: The FastAPI request

    Returns:
        The session from request state
    """
    return request.state.session
