"""Tests for BroadcastManager."""

import pytest
from unittest.mock import AsyncMock
from refast.events.broadcast import BroadcastManager, BroadcastMessage
from refast.events.stream import EventStream, WebSocketConnection


class TestBroadcastMessage:
    """Tests for BroadcastMessage class."""

    def test_broadcast_message_creation(self):
        """Test creating a broadcast message."""
        msg = BroadcastMessage(
            channel="room:1",
            event_type="message",
            data={"text": "Hello"},
        )
        assert msg.channel == "room:1"
        assert msg.event_type == "message"
        assert msg.data["text"] == "Hello"
        assert msg.exclude_session is None

    def test_broadcast_message_with_exclude(self):
        """Test broadcast message with exclusion."""
        msg = BroadcastMessage(
            channel="",
            event_type="notification",
            data={},
            exclude_session="session-123",
        )
        assert msg.exclude_session == "session-123"


class TestBroadcastManager:
    """Tests for BroadcastManager class."""

    def test_init_without_stream(self):
        """Test initialization without stream."""
        broadcaster = BroadcastManager()
        assert broadcaster.stream is None
        assert broadcaster._running is False

    def test_init_with_stream(self):
        """Test initialization with stream."""
        stream = EventStream()
        broadcaster = BroadcastManager(stream)
        assert broadcaster.stream is stream

    @pytest.mark.asyncio
    async def test_broadcast_without_stream(self):
        """Test broadcast without stream returns 0."""
        broadcaster = BroadcastManager()
        count = await broadcaster.broadcast("test:event", {})
        assert count == 0

    @pytest.mark.asyncio
    async def test_broadcast_to_all(self):
        """Test broadcasting to all connections."""
        stream = EventStream()
        broadcaster = BroadcastManager(stream)

        conn1 = WebSocketConnection(connected=True)
        conn1.send = AsyncMock(return_value=True)
        conn2 = WebSocketConnection(connected=True)
        conn2.send = AsyncMock(return_value=True)

        stream._connections[conn1.id] = conn1
        stream._connections[conn2.id] = conn2

        count = await broadcaster.broadcast("test:event", {"value": 1})

        assert count == 2
        conn1.send.assert_called_once()
        conn2.send.assert_called_once()

    @pytest.mark.asyncio
    async def test_broadcast_with_exclude(self):
        """Test broadcasting with session exclusion."""
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
            exclude_session="session1",
        )

        assert count == 1
        conn1.send.assert_not_called()
        conn2.send.assert_called_once()

    @pytest.mark.asyncio
    async def test_broadcast_to_channel(self):
        """Test broadcasting to channel subscribers."""
        stream = EventStream()
        broadcaster = BroadcastManager(stream)

        conn1 = WebSocketConnection(connected=True)
        conn1.subscribe("room:1")
        conn1.send = AsyncMock(return_value=True)

        conn2 = WebSocketConnection(connected=True)
        conn2.send = AsyncMock(return_value=True)

        stream._connections[conn1.id] = conn1
        stream._connections[conn2.id] = conn2

        count = await broadcaster.broadcast_to_channel(
            "room:1",
            "message",
            {"text": "Hello"},
        )

        assert count == 1
        conn1.send.assert_called_once()
        conn2.send.assert_not_called()

    @pytest.mark.asyncio
    async def test_broadcast_to_channel_with_exclude(self):
        """Test channel broadcast with session exclusion."""
        stream = EventStream()
        broadcaster = BroadcastManager(stream)

        conn1 = WebSocketConnection(connected=True, session_id="session1")
        conn1.subscribe("room:1")
        conn1.send = AsyncMock(return_value=True)

        conn2 = WebSocketConnection(connected=True, session_id="session2")
        conn2.subscribe("room:1")
        conn2.send = AsyncMock(return_value=True)

        stream._connections[conn1.id] = conn1
        stream._connections[conn2.id] = conn2

        count = await broadcaster.broadcast_to_channel(
            "room:1",
            "message",
            {},
            exclude_session="session1",
        )

        assert count == 1
        conn1.send.assert_not_called()
        conn2.send.assert_called_once()

    @pytest.mark.asyncio
    async def test_broadcast_to_channel_without_stream(self):
        """Test channel broadcast without stream."""
        broadcaster = BroadcastManager()
        count = await broadcaster.broadcast_to_channel("room:1", "test", {})
        assert count == 0

    @pytest.mark.asyncio
    async def test_broadcast_to_session(self):
        """Test broadcasting to specific session."""
        stream = EventStream()
        broadcaster = BroadcastManager(stream)

        conn1 = WebSocketConnection(connected=True, session_id="session1")
        conn1.send = AsyncMock(return_value=True)
        conn2 = WebSocketConnection(connected=True, session_id="session1")
        conn2.send = AsyncMock(return_value=True)
        conn3 = WebSocketConnection(connected=True, session_id="session2")
        conn3.send = AsyncMock(return_value=True)

        stream._connections[conn1.id] = conn1
        stream._connections[conn2.id] = conn2
        stream._connections[conn3.id] = conn3
        stream._session_connections["session1"] = {conn1.id, conn2.id}
        stream._session_connections["session2"] = {conn3.id}

        count = await broadcaster.broadcast_to_session(
            "session1",
            "notification",
            {"message": "Hello"},
        )

        assert count == 2
        conn1.send.assert_called_once()
        conn2.send.assert_called_once()
        conn3.send.assert_not_called()

    @pytest.mark.asyncio
    async def test_broadcast_to_session_without_stream(self):
        """Test session broadcast without stream."""
        broadcaster = BroadcastManager()
        count = await broadcaster.broadcast_to_session("session1", "test", {})
        assert count == 0

    def test_queue_broadcast(self):
        """Test queuing a broadcast."""
        stream = EventStream()
        broadcaster = BroadcastManager(stream)

        broadcaster.queue_broadcast(
            "room:1",
            "message",
            {"text": "Hello"},
            exclude_session="session1",
        )

        assert not broadcaster._queue.empty()
        msg = broadcaster._queue.get_nowait()
        assert msg.channel == "room:1"
        assert msg.event_type == "message"
        assert msg.data["text"] == "Hello"
        assert msg.exclude_session == "session1"

    @pytest.mark.asyncio
    async def test_start_stop(self):
        """Test starting and stopping the manager."""
        stream = EventStream()
        broadcaster = BroadcastManager(stream)

        await broadcaster.start()
        assert broadcaster._running is True
        assert broadcaster._task is not None

        await broadcaster.stop()
        assert broadcaster._running is False

    @pytest.mark.asyncio
    async def test_start_when_already_running(self):
        """Test starting when already running."""
        stream = EventStream()
        broadcaster = BroadcastManager(stream)

        await broadcaster.start()
        task1 = broadcaster._task

        await broadcaster.start()  # Should be a no-op
        task2 = broadcaster._task

        assert task1 is task2

        await broadcaster.stop()
