"""Tests for event types."""

import pytest
from datetime import datetime
from refast.events.types import (
    Event,
    EventType,
    Callback,
    CallbackEvent,
)


class TestEventType:
    """Tests for EventType enum."""

    def test_callback_type(self):
        """Test CALLBACK event type."""
        assert EventType.CALLBACK == "callback"

    def test_state_update_type(self):
        """Test STATE_UPDATE event type."""
        assert EventType.STATE_UPDATE == "state_update"

    def test_component_update_type(self):
        """Test COMPONENT_UPDATE event type."""
        assert EventType.COMPONENT_UPDATE == "update"

    def test_navigate_type(self):
        """Test NAVIGATE event type."""
        assert EventType.NAVIGATE == "navigate"

    def test_toast_type(self):
        """Test TOAST event type."""
        assert EventType.TOAST == "toast"

    def test_broadcast_type(self):
        """Test BROADCAST event type."""
        assert EventType.BROADCAST == "broadcast"


class TestEvent:
    """Tests for Event class."""

    def test_event_creation(self):
        """Test basic event creation."""
        event = Event(type="user:click", data={"x": 100, "y": 200})
        assert event.type == "user:click"
        assert event.data["x"] == 100
        assert event.data["y"] == 200

    def test_event_defaults(self):
        """Test event default values."""
        event = Event(type="test")
        assert event.data == {}
        assert event.source == "client"
        assert event.session_id is None
        assert event.event_id is not None
        assert isinstance(event.timestamp, datetime)

    def test_event_unique_ids(self):
        """Test events have unique IDs."""
        event1 = Event(type="test")
        event2 = Event(type="test")
        assert event1.event_id != event2.event_id

    def test_event_to_dict(self):
        """Test event serialization."""
        event = Event(type="test", data={"key": "value"})
        d = event.to_dict()
        assert d["type"] == "test"
        assert d["data"]["key"] == "value"
        assert "timestamp" in d
        assert "eventId" in d
        assert d["source"] == "client"

    def test_event_from_dict(self):
        """Test event deserialization."""
        d = {"type": "test", "data": {"a": 1}}
        event = Event.from_dict(d)
        assert event.type == "test"
        assert event.data["a"] == 1

    def test_event_from_dict_with_timestamp(self):
        """Test event deserialization with timestamp."""
        d = {
            "type": "test",
            "data": {},
            "timestamp": "2024-01-01T12:00:00",
        }
        event = Event.from_dict(d)
        assert event.timestamp.year == 2024
        assert event.timestamp.month == 1

    def test_event_from_dict_defaults(self):
        """Test event deserialization with missing fields."""
        d = {}
        event = Event.from_dict(d)
        assert event.type == "unknown"
        assert event.data == {}
        assert event.source == "client"

    def test_event_with_session_id(self):
        """Test event with session ID."""
        event = Event(type="test", session_id="session-123")
        assert event.session_id == "session-123"
        d = event.to_dict()
        assert d["sessionId"] == "session-123"


class TestCallbackEvent:
    """Tests for CallbackEvent class."""

    def test_callback_event_creation(self):
        """Test callback event creation."""
        event = CallbackEvent(
            callback_id="cb-123",
            bound_args={"item_id": 42},
        )
        assert event.callback_id == "cb-123"
        assert event.bound_args["item_id"] == 42

    def test_callback_event_type_set(self):
        """Test callback event type is set automatically."""
        event = CallbackEvent(callback_id="cb-123")
        assert event.type == EventType.CALLBACK


class TestCallback:
    """Tests for Callback class."""

    def test_callback_creation(self):
        """Test basic callback creation."""

        def handler():
            pass

        cb = Callback(id="cb-1", func=handler)
        assert cb.id == "cb-1"
        assert cb.func == handler
        assert cb.bound_args == {}

    def test_callback_with_bound_args(self):
        """Test callback with bound arguments."""

        def handler(ctx, item_id):
            pass

        cb = Callback(id="cb-1", func=handler, bound_args={"item_id": 123})
        assert cb.bound_args["item_id"] == 123

    def test_callback_serialize(self):
        """Test callback serialization."""

        def handler():
            pass

        cb = Callback(id="cb-1", func=handler, bound_args={"id": 123})
        serialized = cb.serialize()
        assert serialized["callbackId"] == "cb-1"
        assert serialized["boundArgs"]["id"] == 123

    def test_callback_with_debounce(self):
        """Test callback with debounce."""

        def handler():
            pass

        cb = Callback(id="cb-1", func=handler, debounce=300)
        serialized = cb.serialize()
        assert serialized["debounce"] == 300
        assert serialized["throttle"] == 0

    def test_callback_with_throttle(self):
        """Test callback with throttle."""

        def handler():
            pass

        cb = Callback(id="cb-1", func=handler, throttle=500)
        serialized = cb.serialize()
        assert serialized["throttle"] == 500

    def test_callback_repr(self):
        """Test callback string representation."""

        def my_handler():
            pass

        cb = Callback(id="cb-1", func=my_handler)
        assert "cb-1" in repr(cb)
        assert "my_handler" in repr(cb)
