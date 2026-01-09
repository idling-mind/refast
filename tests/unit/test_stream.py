"""Tests for WebSocket stream."""

from unittest.mock import AsyncMock

import pytest

from refast.events.stream import EventStream, WebSocketConnection
from refast.events.types import Event


class TestWebSocketConnection:
    """Tests for WebSocketConnection class."""

    def test_connection_has_id(self):
        """Test connection has unique ID."""
        conn = WebSocketConnection()
        assert conn.id is not None
        assert len(conn.id) > 0

    def test_connection_unique_ids(self):
        """Test connections have unique IDs."""
        conn1 = WebSocketConnection()
        conn2 = WebSocketConnection()
        assert conn1.id != conn2.id

    def test_connection_defaults(self):
        """Test connection default values."""
        conn = WebSocketConnection()
        assert conn.websocket is None
        assert conn.session_id is None
        assert conn.subscriptions == set()
        assert conn.connected is False
        assert conn.metadata == {}

    def test_subscribe(self):
        """Test subscribing to a channel."""
        conn = WebSocketConnection()
        conn.subscribe("channel1")
        assert conn.is_subscribed("channel1")

    def test_unsubscribe(self):
        """Test unsubscribing from a channel."""
        conn = WebSocketConnection()
        conn.subscribe("channel1")
        conn.unsubscribe("channel1")
        assert not conn.is_subscribed("channel1")

    def test_unsubscribe_not_subscribed(self):
        """Test unsubscribing when not subscribed."""
        conn = WebSocketConnection()
        # Should not raise
        conn.unsubscribe("unknown")
        assert not conn.is_subscribed("unknown")

    def test_multiple_subscriptions(self):
        """Test multiple channel subscriptions."""
        conn = WebSocketConnection()
        conn.subscribe("channel1")
        conn.subscribe("channel2")
        assert conn.is_subscribed("channel1")
        assert conn.is_subscribed("channel2")
        assert not conn.is_subscribed("channel3")

    @pytest.mark.asyncio
    async def test_send_when_disconnected(self):
        """Test send fails when disconnected."""
        conn = WebSocketConnection(connected=False)
        result = await conn.send({"test": "data"})
        assert result is False

    @pytest.mark.asyncio
    async def test_send_when_no_websocket(self):
        """Test send fails without websocket."""
        conn = WebSocketConnection(connected=True, websocket=None)
        result = await conn.send({"test": "data"})
        assert result is False

    @pytest.mark.asyncio
    async def test_send_success(self):
        """Test successful send."""
        ws = AsyncMock()
        conn = WebSocketConnection(connected=True, websocket=ws)

        result = await conn.send({"test": "data"})

        assert result is True
        ws.send_json.assert_called_once_with({"test": "data"})

    @pytest.mark.asyncio
    async def test_send_error_marks_disconnected(self):
        """Test send error marks connection as disconnected."""
        ws = AsyncMock()
        ws.send_json.side_effect = Exception("Connection closed")
        conn = WebSocketConnection(connected=True, websocket=ws)

        result = await conn.send({"test": "data"})

        assert result is False
        assert conn.connected is False

    @pytest.mark.asyncio
    async def test_send_event(self):
        """Test sending an event."""
        ws = AsyncMock()
        conn = WebSocketConnection(connected=True, websocket=ws)

        event = Event(type="test:event", data={"value": 42})
        result = await conn.send_event(event)

        assert result is True
        ws.send_json.assert_called_once()
        sent_data = ws.send_json.call_args[0][0]
        assert sent_data["type"] == "test:event"
        assert sent_data["data"]["value"] == 42


class TestEventStream:
    """Tests for EventStream class."""

    def test_initial_connection_count(self):
        """Test initial connection count is zero."""
        stream = EventStream()
        assert stream.connection_count == 0

    def test_get_connection_not_found(self):
        """Test getting unknown connection."""
        stream = EventStream()
        assert stream.get_connection("unknown") is None

    def test_get_connection(self):
        """Test getting a registered connection."""
        stream = EventStream()
        conn = WebSocketConnection()
        stream._connections[conn.id] = conn

        result = stream.get_connection(conn.id)
        assert result is conn

    def test_get_session_connections_empty(self):
        """Test getting connections for unknown session."""
        stream = EventStream()
        result = stream.get_session_connections("unknown")
        assert result == []

    def test_get_session_connections(self):
        """Test getting connections for a session."""
        stream = EventStream()

        conn1 = WebSocketConnection(session_id="session1")
        conn2 = WebSocketConnection(session_id="session1")
        conn3 = WebSocketConnection(session_id="session2")

        stream._connections[conn1.id] = conn1
        stream._connections[conn2.id] = conn2
        stream._connections[conn3.id] = conn3
        stream._session_connections["session1"] = {conn1.id, conn2.id}
        stream._session_connections["session2"] = {conn3.id}

        result = stream.get_session_connections("session1")
        assert len(result) == 2
        assert conn1 in result
        assert conn2 in result

    def test_get_all_connections(self):
        """Test getting all connections."""
        stream = EventStream()

        conn1 = WebSocketConnection()
        conn2 = WebSocketConnection()
        stream._connections[conn1.id] = conn1
        stream._connections[conn2.id] = conn2

        result = stream.get_all_connections()
        assert len(result) == 2

    @pytest.mark.asyncio
    async def test_send_to_session(self):
        """Test sending to all session connections."""
        stream = EventStream()

        conn1 = WebSocketConnection(connected=True)
        conn1.send = AsyncMock(return_value=True)
        conn2 = WebSocketConnection(connected=True)
        conn2.send = AsyncMock(return_value=True)

        stream._connections[conn1.id] = conn1
        stream._connections[conn2.id] = conn2
        stream._session_connections["session1"] = {conn1.id, conn2.id}

        count = await stream.send_to_session("session1", {"test": "data"})

        assert count == 2
        conn1.send.assert_called_once()
        conn2.send.assert_called_once()

    @pytest.mark.asyncio
    async def test_send_to_subscribers(self):
        """Test sending to channel subscribers."""
        stream = EventStream()

        conn1 = WebSocketConnection(connected=True)
        conn1.subscribe("channel1")
        conn1.send = AsyncMock(return_value=True)

        conn2 = WebSocketConnection(connected=True)
        conn2.send = AsyncMock(return_value=True)

        stream._connections[conn1.id] = conn1
        stream._connections[conn2.id] = conn2

        count = await stream.send_to_subscribers("channel1", {"test": "data"})

        assert count == 1
        conn1.send.assert_called_once()
        conn2.send.assert_not_called()

    @pytest.mark.asyncio
    async def test_broadcast(self):
        """Test broadcasting to all connections."""
        stream = EventStream()

        conn1 = WebSocketConnection(connected=True)
        conn1.send = AsyncMock(return_value=True)
        conn2 = WebSocketConnection(connected=True)
        conn2.send = AsyncMock(return_value=True)

        stream._connections[conn1.id] = conn1
        stream._connections[conn2.id] = conn2

        count = await stream.broadcast({"test": "data"})

        assert count == 2
        conn1.send.assert_called_once()
        conn2.send.assert_called_once()

    @pytest.mark.asyncio
    async def test_broadcast_partial_failure(self):
        """Test broadcast with some failures."""
        stream = EventStream()

        conn1 = WebSocketConnection(connected=True)
        conn1.send = AsyncMock(return_value=True)
        conn2 = WebSocketConnection(connected=True)
        conn2.send = AsyncMock(return_value=False)

        stream._connections[conn1.id] = conn1
        stream._connections[conn2.id] = conn2

        count = await stream.broadcast({"test": "data"})

        assert count == 1



