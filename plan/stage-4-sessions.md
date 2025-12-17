# Stage 4: Session Management

## Progress

- [x] Task 4.1: Session class
- [x] Task 4.2: Base session store
- [x] Task 4.3: Memory store
- [x] Task 4.4: Redis store
- [x] Task 4.5: Session middleware
- [x] Task 4.6: Session integration

## Objectives

Build session management system:
- Session class with typed data access
- Pluggable session stores (memory, Redis)
- Session middleware for automatic session handling
- Session expiration and cleanup

## Prerequisites

- Stage 1 complete

---

## Task 4.1: Session Class

### Description
Create the Session class for accessing session data.

### Files to Create

**src/refast/session/__init__.py**
```python
"""Session management system."""

from refast.session.session import Session, SessionData
from refast.session.stores.base import SessionStore
from refast.session.stores.memory import MemorySessionStore
from refast.session.middleware import SessionMiddleware

__all__ = [
    "Session",
    "SessionData",
    "SessionStore",
    "MemorySessionStore",
    "SessionMiddleware",
]

# Optional Redis import
try:
    from refast.session.stores.redis import RedisSessionStore
    __all__.append("RedisSessionStore")
except ImportError:
    pass
```

**src/refast/session/session.py**
```python
"""Session class for accessing session data."""

from typing import Any, TypeVar, Generic
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import uuid

from pydantic import BaseModel


T = TypeVar("T", bound=BaseModel)


@dataclass
class SessionData:
    """Raw session data container."""
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    data: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    expires_at: datetime | None = None
    
    def is_expired(self) -> bool:
        """Check if session has expired."""
        if self.expires_at is None:
            return False
        return datetime.utcnow() > self.expires_at
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for storage."""
        return {
            "id": self.id,
            "data": self.data,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
        }
    
    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "SessionData":
        """Create from dictionary."""
        return cls(
            id=d["id"],
            data=d.get("data", {}),
            created_at=datetime.fromisoformat(d["created_at"]),
            updated_at=datetime.fromisoformat(d["updated_at"]),
            expires_at=datetime.fromisoformat(d["expires_at"]) if d.get("expires_at") else None,
        )


class Session(Generic[T]):
    """
    Session interface for accessing session data.
    
    Provides a typed interface to session data with automatic
    persistence through the session store.
    
    Example:
        ```python
        # Simple dict-like access
        ctx.session.set("user_id", 123)
        user_id = ctx.session.get("user_id")
        
        # Typed access with Pydantic model
        class UserSession(BaseModel):
            user_id: int | None = None
            authenticated: bool = False
        
        session = ctx.session.typed(UserSession)
        session.user_id = 123
        session.authenticated = True
        await ctx.session.save()
        ```
    """
    
    def __init__(
        self,
        session_data: SessionData | None = None,
        store: "SessionStore | None" = None,
    ):
        self._data = session_data or SessionData()
        self._store = store
        self._modified = False
    
    @property
    def id(self) -> str:
        """Get session ID."""
        return self._data.id
    
    @property
    def created_at(self) -> datetime:
        """Get session creation time."""
        return self._data.created_at
    
    @property
    def is_modified(self) -> bool:
        """Check if session has been modified."""
        return self._modified
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a value from the session."""
        return self._data.data.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set a value in the session."""
        self._data.data[key] = value
        self._data.updated_at = datetime.utcnow()
        self._modified = True
    
    def delete(self, key: str) -> None:
        """Delete a value from the session."""
        if key in self._data.data:
            del self._data.data[key]
            self._data.updated_at = datetime.utcnow()
            self._modified = True
    
    def clear(self) -> None:
        """Clear all session data."""
        self._data.data.clear()
        self._data.updated_at = datetime.utcnow()
        self._modified = True
    
    def __contains__(self, key: str) -> bool:
        """Check if key exists in session."""
        return key in self._data.data
    
    def __getitem__(self, key: str) -> Any:
        """Dict-like access."""
        return self._data.data[key]
    
    def __setitem__(self, key: str, value: Any) -> None:
        """Dict-like assignment."""
        self.set(key, value)
    
    def keys(self) -> list[str]:
        """Get all session keys."""
        return list(self._data.data.keys())
    
    def values(self) -> list[Any]:
        """Get all session values."""
        return list(self._data.data.values())
    
    def items(self) -> list[tuple[str, Any]]:
        """Get all session items."""
        return list(self._data.data.items())
    
    async def save(self) -> None:
        """Save session to store."""
        if self._store and self._modified:
            await self._store.set(self._data.id, self._data.to_dict())
            self._modified = False
    
    async def destroy(self) -> None:
        """Destroy the session."""
        if self._store:
            await self._store.delete(self._data.id)
        self._data.data.clear()
    
    def set_expiry(self, seconds: int) -> None:
        """Set session expiry time."""
        self._data.expires_at = datetime.utcnow() + timedelta(seconds=seconds)
        self._modified = True
```

### Tests to Write

**tests/unit/test_session.py**
```python
import pytest
from datetime import datetime, timedelta
from refast.session.session import Session, SessionData

class TestSessionData:
    def test_session_data_has_id(self):
        data = SessionData()
        assert data.id is not None
    
    def test_session_data_not_expired_by_default(self):
        data = SessionData()
        assert not data.is_expired()
    
    def test_session_data_expired(self):
        data = SessionData(
            expires_at=datetime.utcnow() - timedelta(hours=1)
        )
        assert data.is_expired()
    
    def test_session_data_to_dict(self):
        data = SessionData(data={"key": "value"})
        d = data.to_dict()
        assert d["data"]["key"] == "value"
        assert "id" in d

class TestSession:
    def test_session_get_set(self):
        session = Session()
        session.set("key", "value")
        assert session.get("key") == "value"
    
    def test_session_get_default(self):
        session = Session()
        assert session.get("missing", "default") == "default"
    
    def test_session_dict_access(self):
        session = Session()
        session["key"] = "value"
        assert session["key"] == "value"
    
    def test_session_contains(self):
        session = Session()
        session.set("key", "value")
        assert "key" in session
        assert "missing" not in session
    
    def test_session_delete(self):
        session = Session()
        session.set("key", "value")
        session.delete("key")
        assert "key" not in session
    
    def test_session_clear(self):
        session = Session()
        session.set("a", 1)
        session.set("b", 2)
        session.clear()
        assert len(session.keys()) == 0
    
    def test_session_modified_flag(self):
        session = Session()
        assert not session.is_modified
        session.set("key", "value")
        assert session.is_modified
```

### Acceptance Criteria

- [ ] Session stores/retrieves data
- [ ] Session has ID and timestamps
- [ ] Session expiry works
- [ ] Modified flag tracks changes

---

## Task 4.2: Base Session Store

### Description
Create the abstract base class for session stores.

### Files to Create

**src/refast/session/stores/__init__.py**
```python
"""Session store implementations."""

from refast.session.stores.base import SessionStore
from refast.session.stores.memory import MemorySessionStore

__all__ = ["SessionStore", "MemorySessionStore"]

try:
    from refast.session.stores.redis import RedisSessionStore
    __all__.append("RedisSessionStore")
except ImportError:
    pass
```

**src/refast/session/stores/base.py**
```python
"""Abstract base class for session stores."""

from abc import ABC, abstractmethod
from typing import Any


class SessionStore(ABC):
    """
    Abstract base class for session storage backends.
    
    Implement this class to create custom session stores.
    
    Example:
        ```python
        class MyStore(SessionStore):
            async def get(self, session_id: str) -> dict | None:
                # Retrieve from your backend
                pass
            
            async def set(self, session_id: str, data: dict, ttl: int = 3600) -> None:
                # Store to your backend
                pass
            
            async def delete(self, session_id: str) -> None:
                # Delete from your backend
                pass
            
            async def exists(self, session_id: str) -> bool:
                # Check existence
                pass
        ```
    """
    
    @abstractmethod
    async def get(self, session_id: str) -> dict[str, Any] | None:
        """
        Retrieve session data by ID.
        
        Args:
            session_id: The session identifier
            
        Returns:
            Session data dict or None if not found
        """
        pass
    
    @abstractmethod
    async def set(
        self,
        session_id: str,
        data: dict[str, Any],
        ttl: int = 3600,
    ) -> None:
        """
        Store session data.
        
        Args:
            session_id: The session identifier
            data: The session data to store
            ttl: Time-to-live in seconds
        """
        pass
    
    @abstractmethod
    async def delete(self, session_id: str) -> None:
        """
        Delete a session.
        
        Args:
            session_id: The session identifier
        """
        pass
    
    @abstractmethod
    async def exists(self, session_id: str) -> bool:
        """
        Check if a session exists.
        
        Args:
            session_id: The session identifier
            
        Returns:
            True if session exists
        """
        pass
    
    async def touch(self, session_id: str, ttl: int = 3600) -> bool:
        """
        Update session TTL without modifying data.
        
        Args:
            session_id: The session identifier
            ttl: New time-to-live in seconds
            
        Returns:
            True if session was touched
        """
        data = await self.get(session_id)
        if data:
            await self.set(session_id, data, ttl)
            return True
        return False
    
    async def clear_expired(self) -> int:
        """
        Clear expired sessions.
        
        Returns:
            Number of sessions cleared
        """
        # Default implementation does nothing
        # Subclasses can override
        return 0
```

### Acceptance Criteria

- [ ] Abstract methods defined
- [ ] Base class is not instantiable
- [ ] touch() helper method works

---

## Task 4.3: Memory Store

### Description
Create an in-memory session store for development.

### Files to Create

**src/refast/session/stores/memory.py**
```python
"""In-memory session store."""

from typing import Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
import asyncio

from refast.session.stores.base import SessionStore


@dataclass
class MemoryEntry:
    """Entry in the memory store."""
    data: dict[str, Any]
    expires_at: datetime


class MemorySessionStore(SessionStore):
    """
    In-memory session store.
    
    Best for development and testing. Not suitable for production
    with multiple workers or server restarts.
    
    Example:
        ```python
        store = MemorySessionStore(default_ttl=3600)
        
        await store.set("session-123", {"user_id": 1})
        data = await store.get("session-123")
        ```
    """
    
    def __init__(
        self,
        default_ttl: int = 3600,
        cleanup_interval: int = 300,
    ):
        self._store: dict[str, MemoryEntry] = {}
        self._default_ttl = default_ttl
        self._cleanup_interval = cleanup_interval
        self._cleanup_task: asyncio.Task | None = None
        self._lock = asyncio.Lock()
    
    async def start_cleanup(self) -> None:
        """Start the periodic cleanup task."""
        if self._cleanup_task is None:
            self._cleanup_task = asyncio.create_task(self._cleanup_loop())
    
    async def stop_cleanup(self) -> None:
        """Stop the periodic cleanup task."""
        if self._cleanup_task:
            self._cleanup_task.cancel()
            try:
                await self._cleanup_task
            except asyncio.CancelledError:
                pass
            self._cleanup_task = None
    
    async def get(self, session_id: str) -> dict[str, Any] | None:
        """Retrieve session data."""
        async with self._lock:
            entry = self._store.get(session_id)
            if entry is None:
                return None
            
            # Check expiration
            if datetime.utcnow() > entry.expires_at:
                del self._store[session_id]
                return None
            
            return entry.data
    
    async def set(
        self,
        session_id: str,
        data: dict[str, Any],
        ttl: int | None = None,
    ) -> None:
        """Store session data."""
        if ttl is None:
            ttl = self._default_ttl
        
        expires_at = datetime.utcnow() + timedelta(seconds=ttl)
        
        async with self._lock:
            self._store[session_id] = MemoryEntry(
                data=data,
                expires_at=expires_at,
            )
    
    async def delete(self, session_id: str) -> None:
        """Delete a session."""
        async with self._lock:
            self._store.pop(session_id, None)
    
    async def exists(self, session_id: str) -> bool:
        """Check if session exists."""
        data = await self.get(session_id)
        return data is not None
    
    async def clear_expired(self) -> int:
        """Clear expired sessions."""
        now = datetime.utcnow()
        count = 0
        
        async with self._lock:
            expired_ids = [
                sid for sid, entry in self._store.items()
                if now > entry.expires_at
            ]
            
            for sid in expired_ids:
                del self._store[sid]
                count += 1
        
        return count
    
    async def clear_all(self) -> None:
        """Clear all sessions (for testing)."""
        async with self._lock:
            self._store.clear()
    
    def session_count(self) -> int:
        """Get number of sessions (for testing)."""
        return len(self._store)
    
    async def _cleanup_loop(self) -> None:
        """Periodic cleanup of expired sessions."""
        while True:
            try:
                await asyncio.sleep(self._cleanup_interval)
                count = await self.clear_expired()
                if count > 0:
                    pass  # Could log this
            except asyncio.CancelledError:
                break
            except Exception:
                pass  # Log error
```

### Tests to Write

**tests/unit/test_memory_store.py**
```python
import pytest
from refast.session.stores.memory import MemorySessionStore

class TestMemorySessionStore:
    @pytest.fixture
    def store(self):
        return MemorySessionStore(default_ttl=60)
    
    @pytest.mark.asyncio
    async def test_set_and_get(self, store):
        await store.set("session-1", {"key": "value"})
        data = await store.get("session-1")
        assert data["key"] == "value"
    
    @pytest.mark.asyncio
    async def test_get_nonexistent(self, store):
        data = await store.get("nonexistent")
        assert data is None
    
    @pytest.mark.asyncio
    async def test_delete(self, store):
        await store.set("session-1", {"key": "value"})
        await store.delete("session-1")
        data = await store.get("session-1")
        assert data is None
    
    @pytest.mark.asyncio
    async def test_exists(self, store):
        await store.set("session-1", {})
        assert await store.exists("session-1")
        assert not await store.exists("nonexistent")
    
    @pytest.mark.asyncio
    async def test_expired_session(self, store):
        # Set with very short TTL
        await store.set("session-1", {"key": "value"}, ttl=0)
        # Should be expired immediately
        import asyncio
        await asyncio.sleep(0.1)
        data = await store.get("session-1")
        assert data is None
    
    @pytest.mark.asyncio
    async def test_clear_expired(self, store):
        await store.set("session-1", {}, ttl=0)
        await store.set("session-2", {}, ttl=3600)
        
        import asyncio
        await asyncio.sleep(0.1)
        
        count = await store.clear_expired()
        assert count == 1
        assert await store.exists("session-2")
```

### Acceptance Criteria

- [ ] Set and get work
- [ ] Expiration works
- [ ] Cleanup task works
- [ ] Thread-safe with locks

---

## Task 4.4: Redis Store

### Description
Create a Redis-based session store for production.

### Files to Create

**src/refast/session/stores/redis.py**
```python
"""Redis session store."""

from typing import Any
import json

from refast.session.stores.base import SessionStore

try:
    import redis.asyncio as redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False


class RedisSessionStore(SessionStore):
    """
    Redis-backed session store.
    
    Suitable for production with multiple workers.
    Requires the `redis` extra: pip install refast[redis]
    
    Example:
        ```python
        store = RedisSessionStore(
            redis_url="redis://localhost:6379/0",
            prefix="refast:session:",
        )
        
        # Or with existing Redis client
        redis_client = redis.from_url("redis://localhost")
        store = RedisSessionStore(client=redis_client)
        ```
    """
    
    def __init__(
        self,
        redis_url: str | None = None,
        client: Any = None,
        prefix: str = "refast:session:",
        default_ttl: int = 3600,
    ):
        if not REDIS_AVAILABLE:
            raise ImportError(
                "Redis is not installed. Install with: pip install refast[redis]"
            )
        
        self._prefix = prefix
        self._default_ttl = default_ttl
        
        if client:
            self._client = client
            self._owned_client = False
        elif redis_url:
            self._client = redis.from_url(redis_url)
            self._owned_client = True
        else:
            raise ValueError("Either redis_url or client must be provided")
    
    def _key(self, session_id: str) -> str:
        """Generate the Redis key for a session."""
        return f"{self._prefix}{session_id}"
    
    async def get(self, session_id: str) -> dict[str, Any] | None:
        """Retrieve session data from Redis."""
        data = await self._client.get(self._key(session_id))
        if data is None:
            return None
        return json.loads(data)
    
    async def set(
        self,
        session_id: str,
        data: dict[str, Any],
        ttl: int | None = None,
    ) -> None:
        """Store session data in Redis."""
        if ttl is None:
            ttl = self._default_ttl
        
        await self._client.setex(
            self._key(session_id),
            ttl,
            json.dumps(data),
        )
    
    async def delete(self, session_id: str) -> None:
        """Delete a session from Redis."""
        await self._client.delete(self._key(session_id))
    
    async def exists(self, session_id: str) -> bool:
        """Check if session exists in Redis."""
        return await self._client.exists(self._key(session_id)) > 0
    
    async def touch(self, session_id: str, ttl: int | None = None) -> bool:
        """Extend session TTL."""
        if ttl is None:
            ttl = self._default_ttl
        
        result = await self._client.expire(self._key(session_id), ttl)
        return result > 0
    
    async def close(self) -> None:
        """Close the Redis connection if owned."""
        if self._owned_client:
            await self._client.close()
```

### Tests to Write

**tests/unit/test_redis_store.py**
```python
import pytest

# Only run if Redis is available
pytest.importorskip("redis")

from refast.session.stores.redis import RedisSessionStore

class TestRedisSessionStore:
    @pytest.fixture
    async def store(self):
        # Use fakeredis for testing
        try:
            import fakeredis.aioredis
            client = fakeredis.aioredis.FakeRedis()
            store = RedisSessionStore(client=client)
            yield store
            await client.flushall()
        except ImportError:
            pytest.skip("fakeredis not available")
    
    @pytest.mark.asyncio
    async def test_set_and_get(self, store):
        await store.set("session-1", {"user": "test"})
        data = await store.get("session-1")
        assert data["user"] == "test"
    
    @pytest.mark.asyncio
    async def test_delete(self, store):
        await store.set("session-1", {})
        await store.delete("session-1")
        assert not await store.exists("session-1")
```

### Acceptance Criteria

- [ ] Redis store works
- [ ] TTL/expiration works
- [ ] Key prefixing works
- [ ] Graceful error on missing Redis

---

## Task 4.5: Session Middleware

### Description
Create middleware that handles session loading and saving.

### Files to Create

**src/refast/session/middleware.py**
```python
"""Session middleware for automatic session handling."""

from typing import Callable, Any, TYPE_CHECKING
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import uuid

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
        call_next: Callable,
    ) -> Response:
        """Process request with session handling."""
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
        """Load session from store or create new one."""
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
    """
    return request.state.session
```

### Tests to Write

**tests/unit/test_session_middleware.py**
```python
import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
from refast.session.middleware import SessionMiddleware, get_session
from refast.session.stores.memory import MemorySessionStore

class TestSessionMiddleware:
    @pytest.fixture
    def app_with_session(self):
        app = FastAPI()
        store = MemorySessionStore()
        app.add_middleware(SessionMiddleware, store=store)
        
        @app.get("/set/{key}/{value}")
        async def set_value(request: Request, key: str, value: str):
            request.state.session.set(key, value)
            return {"set": key}
        
        @app.get("/get/{key}")
        async def get_value(request: Request, key: str):
            return {"value": request.state.session.get(key)}
        
        return app
    
    def test_session_persists(self, app_with_session):
        client = TestClient(app_with_session)
        
        # Set a value
        response = client.get("/set/name/Alice")
        assert response.status_code == 200
        
        # Get the value (same session via cookies)
        response = client.get("/get/name")
        assert response.json()["value"] == "Alice"
    
    def test_session_cookie_set(self, app_with_session):
        client = TestClient(app_with_session)
        response = client.get("/get/anything")
        
        assert "refast_session" in response.cookies
```

### Acceptance Criteria

- [ ] Session loaded from cookie
- [ ] New session created if none
- [ ] Session saved on modification
- [ ] Cookie set correctly

---

## Task 4.6: Integration with Context

### Description
Integrate session with the Context class.

### Updates to src/refast/context.py

Add session integration:
```python
# In Context.__init__
self._session: Session | None = None

# Add session property
@property
def session(self) -> Session:
    """Access the session."""
    if self._session is None:
        # Try to get from request
        if self._request and hasattr(self._request.state, "session"):
            self._session = self._request.state.session
        else:
            # Create empty session
            from refast.session import Session
            self._session = Session()
    return self._session

@session.setter
def session(self, value: Session) -> None:
    """Set the session."""
    self._session = value
```

### Acceptance Criteria

- [ ] Context has session property
- [ ] Session accessible in callbacks
- [ ] Session persists across requests

---

## Final Checklist for Stage 4

- [ ] Session class complete
- [ ] Memory store complete
- [ ] Redis store complete
- [ ] Middleware complete
- [ ] Integration with Context
- [ ] All tests pass
- [ ] Update `.github/copilot-instructions.md` status to 🟢
