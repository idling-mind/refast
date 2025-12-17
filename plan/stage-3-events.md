# Stage 3: Event Handling & WebSocket

## Progress

- [x] Task 3.1: Event type definitions
- [x] Task 3.2: Event manager
- [x] Task 3.3: WebSocket streaming
- [x] Task 3.4: Broadcast manager
- [x] Task 3.5: Client subscriptions
- [x] Task 3.6: Event flow utilities

## Objectives

Build the real-time event system:
- Event type definitions and validation
- WebSocket connection management
- Event streaming (frontend ↔ backend)
- Broadcast to all clients
- Client subscription to event channels

## Prerequisites

- Stage 1 complete
- Stage 2 complete (components needed for events)

---

## Task 3.1: Event Type Definitions

### Description
Define event types and data structures.

### Files to Create

**src/refast/events/__init__.py**
```python
"""Event handling system."""

from refast.events.types import Event, EventHandler, Callback
from refast.events.manager import EventManager
from refast.events.stream import EventStream, WebSocketConnection
from refast.events.broadcast import BroadcastManager

__all__ = [
    "Event",
    "EventHandler",
    "Callback",
    "EventManager",
    "EventStream",
    "WebSocketConnection",
    "BroadcastManager",
]
```

**src/refast/events/types.py**
```python
"""Event type definitions."""

from typing import Any, Callable, Awaitable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import uuid


class EventType(str, Enum):
    """Built-in event types."""
    CALLBACK = "callback"
    STATE_UPDATE = "state_update"
    COMPONENT_UPDATE = "update"
    NAVIGATE = "navigate"
    TOAST = "toast"
    MODAL = "modal"
    BROADCAST = "broadcast"
    CUSTOM = "custom"


@dataclass
class Event:
    """
    Represents an event in the system.
    
    Events can flow from frontend to backend (user interactions)
    or from backend to frontend (updates, broadcasts).
    
    Example:
        ```python
        @ui.on_event("user:click")
        async def handle_click(ctx: Context, event: Event):
            print(f"Clicked: {event.data}")
        ```
    """
    
    type: str
    data: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.utcnow)
    source: str = "client"  # "client" or "server"
    session_id: str | None = None
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    
    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "type": self.type,
            "data": self.data,
            "timestamp": self.timestamp.isoformat(),
            "source": self.source,
            "sessionId": self.session_id,
            "eventId": self.event_id,
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Event":
        """Create Event from dictionary."""
        return cls(
            type=data.get("type", "unknown"),
            data=data.get("data", {}),
            timestamp=datetime.fromisoformat(data["timestamp"]) if "timestamp" in data else datetime.utcnow(),
            source=data.get("source", "client"),
            session_id=data.get("sessionId"),
            event_id=data.get("eventId", str(uuid.uuid4())),
        )


@dataclass
class CallbackEvent(Event):
    """Event for invoking a callback."""
    
    callback_id: str = ""
    bound_args: dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        self.type = EventType.CALLBACK


# Type alias for event handlers
EventHandler = Callable[["Context", Event], Awaitable[Any]]


@dataclass
class Callback:
    """
    Represents a callback that can be triggered from the frontend.
    
    Example:
        ```python
        cb = ctx.callback(handle_click, item_id=123)
        Button("Click", on_click=cb)
        ```
    """
    
    id: str
    func: Callable
    bound_args: dict[str, Any] = field(default_factory=dict)
    debounce: int = 0  # Milliseconds to debounce
    throttle: int = 0  # Milliseconds to throttle
    
    def serialize(self) -> dict[str, Any]:
        """Serialize for sending to frontend."""
        return {
            "callbackId": self.id,
            "boundArgs": self.bound_args,
            "debounce": self.debounce,
            "throttle": self.throttle,
        }
    
    def __repr__(self) -> str:
        return f"Callback(id={self.id!r}, func={self.func.__name__!r})"
```

### Tests to Write

**tests/unit/test_events.py**
```python
import pytest
from refast.events.types import Event, Callback, CallbackEvent

class TestEvent:
    def test_event_creation(self):
        event = Event(type="user:click", data={"x": 100, "y": 200})
        assert event.type == "user:click"
        assert event.data["x"] == 100
    
    def test_event_to_dict(self):
        event = Event(type="test", data={"key": "value"})
        d = event.to_dict()
        assert d["type"] == "test"
        assert "timestamp" in d
        assert "eventId" in d
    
    def test_event_from_dict(self):
        d = {"type": "test", "data": {"a": 1}}
        event = Event.from_dict(d)
        assert event.type == "test"
        assert event.data["a"] == 1

class TestCallback:
    def test_callback_serialize(self):
        def handler():
            pass
        cb = Callback(id="cb-1", func=handler, bound_args={"id": 123})
        serialized = cb.serialize()
        assert serialized["callbackId"] == "cb-1"
        assert serialized["boundArgs"]["id"] == 123
    
    def test_callback_with_debounce(self):
        def handler():
            pass
        cb = Callback(id="cb-1", func=handler, debounce=300)
        serialized = cb.serialize()
        assert serialized["debounce"] == 300
```

### Acceptance Criteria

- [ ] Event class works with serialization
- [ ] Callback class serializes correctly
- [ ] Event types defined

---

## Task 3.2: Event Manager

### Description
Create the central event routing and handling system.

### Files to Create

**src/refast/events/manager.py**
```python
"""Event manager for routing events."""

from typing import Any, Callable, Awaitable, TYPE_CHECKING
from collections import defaultdict
import asyncio
import logging

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
        self.app = app
        self._handlers: dict[str, list[EventHandler]] = defaultdict(list)
        self._callbacks: dict[str, Callable] = {}
        self._middleware: list[Callable] = []
    
    def on(self, event_type: str) -> Callable[[EventHandler], EventHandler]:
        """Decorator to register an event handler."""
        def decorator(func: EventHandler) -> EventHandler:
            self._handlers[event_type].append(func)
            return func
        return decorator
    
    def register_handler(self, event_type: str, handler: EventHandler) -> None:
        """Register an event handler programmatically."""
        self._handlers[event_type].append(handler)
    
    def unregister_handler(self, event_type: str, handler: EventHandler) -> None:
        """Remove an event handler."""
        if event_type in self._handlers:
            self._handlers[event_type] = [
                h for h in self._handlers[event_type] if h != handler
            ]
    
    def register_callback(self, callback_id: str, func: Callable) -> None:
        """Register a callback function."""
        self._callbacks[callback_id] = func
    
    def get_callback(self, callback_id: str) -> Callable | None:
        """Get a registered callback."""
        return self._callbacks.get(callback_id)
    
    def add_middleware(self, middleware: Callable) -> None:
        """
        Add middleware that runs before event handlers.
        
        Middleware signature: async def middleware(ctx, event, next) -> Any
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
        """Run handler with middleware chain."""
        if not self._middleware:
            return await handler(ctx, event)
        
        # Build middleware chain
        async def run_handler(c, e):
            return await handler(c, e)
        
        chain = run_handler
        for middleware in reversed(self._middleware):
            chain = self._wrap_middleware(middleware, chain)
        
        return await chain(ctx, event)
    
    def _wrap_middleware(
        self,
        middleware: Callable,
        next_handler: Callable,
    ) -> Callable:
        """Wrap a middleware function."""
        async def wrapped(ctx, event):
            return await middleware(ctx, event, next_handler)
        return wrapped
```

### Tests to Write

**tests/unit/test_event_manager.py**
```python
import pytest
from refast.events.manager import EventManager
from refast.events.types import Event

class TestEventManager:
    @pytest.mark.asyncio
    async def test_register_and_emit(self):
        manager = EventManager()
        results = []
        
        @manager.on("test:event")
        async def handler(ctx, event):
            results.append(event.data)
        
        await manager.emit("test:event", {"value": 42})
        assert len(results) == 1
        assert results[0]["value"] == 42
    
    @pytest.mark.asyncio
    async def test_multiple_handlers(self):
        manager = EventManager()
        results = []
        
        @manager.on("test:event")
        async def handler1(ctx, event):
            results.append("handler1")
        
        @manager.on("test:event")
        async def handler2(ctx, event):
            results.append("handler2")
        
        await manager.emit("test:event", {})
        assert results == ["handler1", "handler2"]
    
    @pytest.mark.asyncio
    async def test_callback_invocation(self):
        manager = EventManager()
        
        async def my_callback(ctx, item_id: int):
            return item_id * 2
        
        manager.register_callback("cb-1", my_callback)
        
        result = await manager.invoke_callback(
            "cb-1",
            ctx=None,
            event_data={"boundArgs": {"item_id": 21}}
        )
        assert result == 42
    
    @pytest.mark.asyncio
    async def test_middleware(self):
        manager = EventManager()
        order = []
        
        async def middleware1(ctx, event, next):
            order.append("m1-before")
            result = await next(ctx, event)
            order.append("m1-after")
            return result
        
        manager.add_middleware(middleware1)
        
        @manager.on("test")
        async def handler(ctx, event):
            order.append("handler")
        
        await manager.emit("test", {})
        assert order == ["m1-before", "handler", "m1-after"]
```

### Acceptance Criteria

- [ ] Event handlers can be registered
- [ ] Events emit to all handlers
- [ ] Callbacks can be invoked
- [ ] Middleware works

---

## Task 3.3: WebSocket Streaming

### Description
Create WebSocket connection management and streaming.

### Files to Create

**src/refast/events/stream.py**
```python
"""WebSocket streaming and connection management."""

from typing import Any, TYPE_CHECKING
from dataclasses import dataclass, field
from contextlib import asynccontextmanager
import asyncio
import json
import logging
import uuid

from fastapi import WebSocket, WebSocketDisconnect

from refast.events.types import Event

if TYPE_CHECKING:
    from refast.app import RefastApp
    from refast.session import Session

logger = logging.getLogger(__name__)


@dataclass
class WebSocketConnection:
    """
    Represents a WebSocket connection.
    
    Tracks connection state, session, and subscriptions.
    """
    
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    websocket: WebSocket | None = None
    session_id: str | None = None
    subscriptions: set[str] = field(default_factory=set)
    connected: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)
    
    async def send(self, data: dict[str, Any]) -> bool:
        """Send data to the client."""
        if not self.connected or not self.websocket:
            return False
        
        try:
            await self.websocket.send_json(data)
            return True
        except Exception as e:
            logger.error(f"Error sending to connection {self.id}: {e}")
            self.connected = False
            return False
    
    async def send_event(self, event: Event) -> bool:
        """Send an event to the client."""
        return await self.send(event.to_dict())
    
    def subscribe(self, channel: str) -> None:
        """Subscribe to an event channel."""
        self.subscriptions.add(channel)
    
    def unsubscribe(self, channel: str) -> None:
        """Unsubscribe from an event channel."""
        self.subscriptions.discard(channel)
    
    def is_subscribed(self, channel: str) -> bool:
        """Check if subscribed to a channel."""
        return channel in self.subscriptions


class EventStream:
    """
    Manages WebSocket connections and event streaming.
    
    Provides:
    - Connection lifecycle management
    - Message routing
    - Stream-based event delivery
    
    Example:
        ```python
        stream = EventStream(app)
        
        async with stream.connection(websocket) as conn:
            async for message in stream.receive(conn):
                await stream.handle_message(conn, message)
        ```
    """
    
    def __init__(self, app: "RefastApp | None" = None):
        self.app = app
        self._connections: dict[str, WebSocketConnection] = {}
        self._session_connections: dict[str, set[str]] = {}
    
    @property
    def connection_count(self) -> int:
        """Number of active connections."""
        return len(self._connections)
    
    def get_connection(self, connection_id: str) -> WebSocketConnection | None:
        """Get a connection by ID."""
        return self._connections.get(connection_id)
    
    def get_session_connections(self, session_id: str) -> list[WebSocketConnection]:
        """Get all connections for a session."""
        conn_ids = self._session_connections.get(session_id, set())
        return [
            self._connections[cid]
            for cid in conn_ids
            if cid in self._connections
        ]
    
    @asynccontextmanager
    async def connection(self, websocket: WebSocket, session_id: str | None = None):
        """
        Context manager for WebSocket connection lifecycle.
        
        Example:
            ```python
            async with stream.connection(websocket, session_id) as conn:
                # Connection is active
                await process_messages(conn)
            # Connection is automatically cleaned up
            ```
        """
        conn = WebSocketConnection(
            websocket=websocket,
            session_id=session_id,
        )
        
        try:
            await websocket.accept()
            conn.connected = True
            
            # Register connection
            self._connections[conn.id] = conn
            if session_id:
                if session_id not in self._session_connections:
                    self._session_connections[session_id] = set()
                self._session_connections[session_id].add(conn.id)
            
            logger.info(f"WebSocket connected: {conn.id}")
            yield conn
            
        except WebSocketDisconnect:
            logger.info(f"WebSocket disconnected: {conn.id}")
        except Exception as e:
            logger.error(f"WebSocket error: {e}")
        finally:
            # Cleanup
            conn.connected = False
            self._connections.pop(conn.id, None)
            if session_id and session_id in self._session_connections:
                self._session_connections[session_id].discard(conn.id)
            logger.info(f"WebSocket cleaned up: {conn.id}")
    
    async def receive(self, conn: WebSocketConnection):
        """
        Async generator to receive messages from a connection.
        
        Example:
            ```python
            async for message in stream.receive(conn):
                await handle_message(message)
            ```
        """
        if not conn.websocket:
            return
        
        try:
            while conn.connected:
                data = await conn.websocket.receive_json()
                yield data
        except WebSocketDisconnect:
            conn.connected = False
        except Exception as e:
            logger.error(f"Error receiving from {conn.id}: {e}")
            conn.connected = False
    
    async def send_to_session(
        self,
        session_id: str,
        data: dict[str, Any],
    ) -> int:
        """
        Send data to all connections for a session.
        
        Returns number of successful sends.
        """
        connections = self.get_session_connections(session_id)
        success_count = 0
        
        for conn in connections:
            if await conn.send(data):
                success_count += 1
        
        return success_count
    
    async def send_to_subscribers(
        self,
        channel: str,
        data: dict[str, Any],
    ) -> int:
        """
        Send data to all connections subscribed to a channel.
        
        Returns number of successful sends.
        """
        success_count = 0
        
        for conn in self._connections.values():
            if conn.is_subscribed(channel):
                if await conn.send(data):
                    success_count += 1
        
        return success_count
```

### Tests to Write

**tests/unit/test_stream.py**
```python
import pytest
from unittest.mock import AsyncMock, MagicMock
from refast.events.stream import EventStream, WebSocketConnection

class TestWebSocketConnection:
    def test_connection_has_id(self):
        conn = WebSocketConnection()
        assert conn.id is not None
    
    def test_subscribe_unsubscribe(self):
        conn = WebSocketConnection()
        conn.subscribe("channel1")
        assert conn.is_subscribed("channel1")
        
        conn.unsubscribe("channel1")
        assert not conn.is_subscribed("channel1")
    
    @pytest.mark.asyncio
    async def test_send_when_disconnected(self):
        conn = WebSocketConnection(connected=False)
        result = await conn.send({"test": "data"})
        assert result is False

class TestEventStream:
    def test_connection_count(self):
        stream = EventStream()
        assert stream.connection_count == 0
    
    def test_get_connection(self):
        stream = EventStream()
        conn = WebSocketConnection()
        stream._connections[conn.id] = conn
        
        result = stream.get_connection(conn.id)
        assert result is conn
```

### Acceptance Criteria

- [ ] WebSocket connections managed
- [ ] Message receiving works
- [ ] Session-based messaging works
- [ ] Subscription-based messaging works

---

## Task 3.4: Broadcast Manager

### Description
Create broadcasting system for sending events to all clients.

### Files to Create

**src/refast/events/broadcast.py**
```python
"""Broadcast manager for sending events to all clients."""

from typing import Any, TYPE_CHECKING
from dataclasses import dataclass
import asyncio
import logging

from refast.events.types import Event
from refast.events.stream import EventStream

if TYPE_CHECKING:
    from refast.app import RefastApp

logger = logging.getLogger(__name__)


@dataclass
class BroadcastMessage:
    """A message to broadcast."""
    channel: str
    event_type: str
    data: dict[str, Any]
    exclude_session: str | None = None


class BroadcastManager:
    """
    Manages broadcasting events to all connected clients.
    
    Supports:
    - Broadcast to all clients
    - Broadcast to specific channels
    - Exclude specific sessions
    
    Example:
        ```python
        broadcaster = BroadcastManager(stream)
        
        # Broadcast to all
        await broadcaster.broadcast("notification", {"message": "Hello everyone!"})
        
        # Broadcast to channel subscribers
        await broadcaster.broadcast_to_channel("room:123", "message", {"text": "Hi room!"})
        ```
    """
    
    def __init__(self, stream: EventStream | None = None):
        self.stream = stream
        self._queue: asyncio.Queue[BroadcastMessage] = asyncio.Queue()
        self._running = False
        self._task: asyncio.Task | None = None
    
    async def start(self) -> None:
        """Start the broadcast processor."""
        if self._running:
            return
        
        self._running = True
        self._task = asyncio.create_task(self._process_queue())
        logger.info("Broadcast manager started")
    
    async def stop(self) -> None:
        """Stop the broadcast processor."""
        self._running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        logger.info("Broadcast manager stopped")
    
    async def broadcast(
        self,
        event_type: str,
        data: dict[str, Any],
        exclude_session: str | None = None,
    ) -> int:
        """
        Broadcast an event to all connected clients.
        
        Args:
            event_type: Type of event to broadcast
            data: Event data
            exclude_session: Optional session to exclude
            
        Returns:
            Number of clients that received the broadcast
        """
        if not self.stream:
            logger.warning("No stream configured for broadcast")
            return 0
        
        event = Event(
            type=event_type,
            data=data,
            source="server",
        )
        
        count = 0
        for conn in self.stream._connections.values():
            if exclude_session and conn.session_id == exclude_session:
                continue
            
            if await conn.send_event(event):
                count += 1
        
        logger.debug(f"Broadcast {event_type} to {count} clients")
        return count
    
    async def broadcast_to_channel(
        self,
        channel: str,
        event_type: str,
        data: dict[str, Any],
        exclude_session: str | None = None,
    ) -> int:
        """
        Broadcast to clients subscribed to a specific channel.
        
        Args:
            channel: The channel name
            event_type: Type of event
            data: Event data
            exclude_session: Optional session to exclude
            
        Returns:
            Number of clients that received the broadcast
        """
        if not self.stream:
            return 0
        
        event = Event(
            type=event_type,
            data=data,
            source="server",
        )
        
        count = 0
        for conn in self.stream._connections.values():
            if exclude_session and conn.session_id == exclude_session:
                continue
            
            if conn.is_subscribed(channel):
                if await conn.send_event(event):
                    count += 1
        
        return count
    
    def queue_broadcast(
        self,
        channel: str,
        event_type: str,
        data: dict[str, Any],
        exclude_session: str | None = None,
    ) -> None:
        """Queue a broadcast for async processing."""
        message = BroadcastMessage(
            channel=channel,
            event_type=event_type,
            data=data,
            exclude_session=exclude_session,
        )
        self._queue.put_nowait(message)
    
    async def _process_queue(self) -> None:
        """Process queued broadcasts."""
        while self._running:
            try:
                message = await asyncio.wait_for(
                    self._queue.get(),
                    timeout=1.0,
                )
                
                if message.channel:
                    await self.broadcast_to_channel(
                        message.channel,
                        message.event_type,
                        message.data,
                        message.exclude_session,
                    )
                else:
                    await self.broadcast(
                        message.event_type,
                        message.data,
                        message.exclude_session,
                    )
                
            except asyncio.TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Error processing broadcast: {e}")
```

### Tests to Write

**tests/unit/test_broadcast.py**
```python
import pytest
from unittest.mock import AsyncMock
from refast.events.broadcast import BroadcastManager
from refast.events.stream import EventStream, WebSocketConnection

class TestBroadcastManager:
    @pytest.mark.asyncio
    async def test_broadcast_to_all(self):
        stream = EventStream()
        broadcaster = BroadcastManager(stream)
        
        # Add mock connections
        conn1 = WebSocketConnection(connected=True)
        conn1.send = AsyncMock(return_value=True)
        conn2 = WebSocketConnection(connected=True)
        conn2.send = AsyncMock(return_value=True)
        
        stream._connections[conn1.id] = conn1
        stream._connections[conn2.id] = conn2
        
        count = await broadcaster.broadcast("test:event", {"value": 1})
        assert count == 2
    
    @pytest.mark.asyncio
    async def test_broadcast_with_exclude(self):
        stream = EventStream()
        broadcaster = BroadcastManager(stream)
        
        conn1 = WebSocketConnection(connected=True, session_id="session1")
        conn1.send = AsyncMock(return_value=True)
        conn2 = WebSocketConnection(connected=True, session_id="session2")
        conn2.send = AsyncMock(return_value=True)
        
        stream._connections[conn1.id] = conn1
        stream._connections[conn2.id] = conn2
        
        count = await broadcaster.broadcast(
            "test:event",
            {},
            exclude_session="session1"
        )
        assert count == 1
        conn2.send.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_broadcast_to_channel(self):
        stream = EventStream()
        broadcaster = BroadcastManager(stream)
        
        conn1 = WebSocketConnection(connected=True)
        conn1.subscribe("room:1")
        conn1.send = AsyncMock(return_value=True)
        
        conn2 = WebSocketConnection(connected=True)
        conn2.send = AsyncMock(return_value=True)
        
        stream._connections[conn1.id] = conn1
        stream._connections[conn2.id] = conn2
        
        count = await broadcaster.broadcast_to_channel("room:1", "message", {})
        assert count == 1
        conn1.send.assert_called_once()
        conn2.send.assert_not_called()
```

### Acceptance Criteria

- [ ] Broadcast to all clients works
- [ ] Channel-based broadcast works
- [ ] Session exclusion works
- [ ] Queue-based broadcast works

---

## Task 3.5: Client Subscriptions

### Description
Add subscription management components and handlers.

### Files to Add

Add to context.py:
```python
async def subscribe(self, channel: str) -> None:
    """Subscribe the current connection to a channel."""
    if self._websocket and hasattr(self, '_connection'):
        self._connection.subscribe(channel)

async def unsubscribe(self, channel: str) -> None:
    """Unsubscribe from a channel."""
    if self._websocket and hasattr(self, '_connection'):
        self._connection.unsubscribe(channel)
```

Create EventSubscriber component for frontend:
```python
# In components/shadcn/events.py
class EventSubscriber(Component):
    """Component that subscribes to events."""
    
    component_type: str = "EventSubscriber"
    
    def __init__(
        self,
        events: list[str],
        on_event: Any = None,
        id: str | None = None,
    ):
        super().__init__(id=id)
        self.events = events
        self.on_event = on_event
    
    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "events": self.events,
                "onEvent": self.on_event.serialize() if self.on_event else None,
            },
            "children": [],
        }
```

### Acceptance Criteria

- [ ] Clients can subscribe to channels
- [ ] EventSubscriber component works
- [ ] Subscription state persists

---

## Task 3.6: Integration Tests

### Files to Create

**tests/integration/test_websocket.py**
```python
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from refast import RefastApp

class TestWebSocketIntegration:
    @pytest.fixture
    def app_with_events(self):
        app = FastAPI()
        ui = RefastApp()
        
        @ui.on_event("ping")
        async def handle_ping(ctx, event):
            await ctx.push_event("pong", {"received": event.data})
        
        app.include_router(ui.router, prefix="/ui")
        return app
    
    def test_websocket_connects(self, app_with_events):
        client = TestClient(app_with_events)
        with client.websocket_connect("/ui/ws") as websocket:
            # Connection successful
            assert True
    
    def test_websocket_ping_pong(self, app_with_events):
        client = TestClient(app_with_events)
        with client.websocket_connect("/ui/ws") as websocket:
            websocket.send_json({
                "type": "event",
                "eventType": "ping",
                "data": {"message": "hello"}
            })
            # Would receive pong response
```

---

## Final Checklist for Stage 3

- [ ] Event types defined
- [ ] Event manager routes events
- [ ] WebSocket connections managed
- [ ] Broadcasting works
- [ ] Subscriptions work
- [ ] Integration tests pass
- [ ] Update `.github/copilot-instructions.md` status to 🟢
