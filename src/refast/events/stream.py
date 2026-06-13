"""WebSocket streaming and connection management."""

import logging
import uuid
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from fastapi import WebSocket, WebSocketDisconnect

from refast.events.types import Event

if TYPE_CHECKING:
    from refast.app import RefastApp

logger = logging.getLogger(__name__)


@dataclass
class WebSocketConnection:
    """
    Represents a WebSocket connection.

    Tracks connection state, session, and subscriptions.

    Attributes:
        id: Unique identifier for this connection
        websocket: The FastAPI WebSocket instance
        session_id: Session ID if authenticated
        subscriptions: Set of channels the connection is subscribed to
        connected: Whether the connection is active
        metadata: Additional connection metadata
    """

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    websocket: WebSocket | None = None
    session_id: str | None = None
    subscriptions: set[str] = field(default_factory=set)
    connected: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    async def send(self, data: dict[str, Any]) -> bool:
        """
        Send data to the client.

        Args:
            data: The data to send

        Returns:
            True if successful, False otherwise
        """
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
        """
        Send an event to the client.

        Args:
            event: The event to send

        Returns:
            True if successful, False otherwise
        """
        return await self.send(event.to_dict())

    def subscribe(self, channel: str) -> None:
        """
        Subscribe to an event channel.

        Args:
            channel: The channel name
        """
        self.subscriptions.add(channel)

    def unsubscribe(self, channel: str) -> None:
        """
        Unsubscribe from an event channel.

        Args:
            channel: The channel name
        """
        self.subscriptions.discard(channel)

    def is_subscribed(self, channel: str) -> bool:
        """
        Check if subscribed to a channel.

        Args:
            channel: The channel name

        Returns:
            True if subscribed
        """
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
        """
        Initialize the event stream.

        Args:
            app: Optional RefastApp instance
        """
        self.app = app
        self._connections: dict[str, WebSocketConnection] = {}
        self._session_connections: dict[str, set[str]] = {}

    @property
    def connection_count(self) -> int:
        """Number of active connections."""
        return len(self._connections)

    def get_connection(self, connection_id: str) -> WebSocketConnection | None:
        """
        Get a connection by ID.

        Args:
            connection_id: The connection ID

        Returns:
            The connection or None
        """
        return self._connections.get(connection_id)

    def get_session_connections(self, session_id: str) -> list[WebSocketConnection]:
        """
        Get all connections for a session.

        Args:
            session_id: The session ID

        Returns:
            List of connections for the session
        """
        conn_ids = self._session_connections.get(session_id, set())
        return [self._connections[cid] for cid in conn_ids if cid in self._connections]

    def get_all_connections(self) -> list[WebSocketConnection]:
        """
        Get all active connections.

        Returns:
            List of all connections
        """
        return list(self._connections.values())

    @asynccontextmanager
    async def connection(
        self, websocket: WebSocket, session_id: str | None = None
    ) -> AsyncIterator[WebSocketConnection]:
        """
        Context manager for WebSocket connection lifecycle.

        Example:
            ```python
            async with stream.connection(websocket, session_id) as conn:
                # Connection is active
                await process_messages(conn)
            # Connection is automatically cleaned up
            ```

        Args:
            websocket: The FastAPI WebSocket
            session_id: Optional session ID

        Yields:
            The WebSocket connection
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

    async def receive(self, conn: WebSocketConnection) -> AsyncIterator[dict[str, Any]]:
        """
        Async generator to receive messages from a connection.

        Example:
            ```python
            async for message in stream.receive(conn):
                await handle_message(message)
            ```

        Args:
            conn: The WebSocket connection

        Yields:
            Received messages as dictionaries
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

        Args:
            session_id: The session ID
            data: The data to send

        Returns:
            Number of successful sends
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

        Args:
            channel: The channel name
            data: The data to send

        Returns:
            Number of successful sends
        """
        success_count = 0

        for conn in self._connections.values():
            if conn.is_subscribed(channel):
                if await conn.send(data):
                    success_count += 1

        return success_count

    async def broadcast(self, data: dict[str, Any]) -> int:
        """
        Broadcast data to all connected clients.

        Args:
            data: The data to send

        Returns:
            Number of successful sends
        """
        success_count = 0

        for conn in self._connections.values():
            if await conn.send(data):
                success_count += 1

        return success_count
