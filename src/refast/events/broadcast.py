"""Broadcast manager for sending events to all clients."""

import asyncio
import logging
from dataclasses import dataclass
from typing import Any

from refast.events.stream import EventStream
from refast.events.types import Event

logger = logging.getLogger(__name__)


@dataclass
class BroadcastMessage:
    """
    A message to broadcast.

    Attributes:
        channel: The channel to broadcast to (empty for all)
        event_type: The type of event
        data: The event data
        exclude_session: Session ID to exclude from broadcast
    """

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
        await broadcaster.broadcast_to_channel(
            "room:123", "message", {"text": "Hi room!"}
        )
        ```
    """

    def __init__(self, stream: EventStream | None = None):
        """
        Initialize the broadcast manager.

        Args:
            stream: The EventStream for WebSocket connections
        """
        self.stream = stream
        self._queue: asyncio.Queue[BroadcastMessage] = asyncio.Queue()
        self._running = False
        self._task: asyncio.Task[None] | None = None

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

    async def broadcast_to_session(
        self,
        session_id: str,
        event_type: str,
        data: dict[str, Any],
    ) -> int:
        """
        Send an event to all connections for a specific session.

        Args:
            session_id: The session ID
            event_type: Type of event
            data: Event data

        Returns:
            Number of connections that received the event
        """
        if not self.stream:
            return 0

        event = Event(
            type=event_type,
            data=data,
            source="server",
        )

        count = 0
        for conn in self.stream.get_session_connections(session_id):
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
        """
        Queue a broadcast for async processing.

        Args:
            channel: The channel (empty for all clients)
            event_type: Type of event
            data: Event data
            exclude_session: Optional session to exclude
        """
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

            except TimeoutError:
                continue
            except Exception as e:
                logger.error(f"Error processing broadcast: {e}")
