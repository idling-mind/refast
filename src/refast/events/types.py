"""Event type definitions."""

import uuid
from collections.abc import Awaitable, Callable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from refast.context import Context


def _now_utc() -> datetime:
    """Get current UTC time."""
    return datetime.now(UTC)


class EventType(StrEnum):
    """Built-in event types."""

    CALLBACK = "callback"
    STATE_UPDATE = "state_update"
    COMPONENT_UPDATE = "update"
    NAVIGATE = "navigate"
    TOAST = "toast"
    MODAL = "modal"
    BROADCAST = "broadcast"
    STORE_INIT = "store_init"
    STORE_UPDATE = "store_update"
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

    Attributes:
        type: The event type (e.g., "user:click")
        data: The event payload data
        timestamp: When the event was created
        source: Where the event originated ("client" or "server")
        session_id: The session ID if applicable
        event_id: Unique identifier for this event
    """

    type: str
    data: dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=_now_utc)
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
            timestamp=(
                datetime.fromisoformat(data["timestamp"]) if "timestamp" in data else _now_utc()
            ),
            source=data.get("source", "client"),
            session_id=data.get("sessionId"),
            event_id=data.get("eventId", str(uuid.uuid4())),
        )


@dataclass
class CallbackEvent(Event):
    """Event for invoking a callback."""

    type: str = field(default=EventType.CALLBACK)  # type: ignore[assignment]
    callback_id: str = ""
    bound_args: dict[str, Any] = field(default_factory=dict)


# Type alias for event handlers
EventHandler = Callable[["Context", Event], Awaitable[Any]]
