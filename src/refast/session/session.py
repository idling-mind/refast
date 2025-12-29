"""Session class for accessing session data."""

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from refast.session.stores.base import SessionStore


def _now_utc() -> datetime:
    """Get current UTC time."""
    return datetime.now(UTC)


@dataclass
class SessionData:
    """
    Raw session data container.

    Attributes:
        id: Unique session identifier
        data: The session key-value data
        created_at: When the session was created
        updated_at: When the session was last updated
        expires_at: When the session expires (None for no expiry)
    """

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    data: dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=_now_utc)
    updated_at: datetime = field(default_factory=_now_utc)
    expires_at: datetime | None = None

    def is_expired(self) -> bool:
        """Check if session has expired."""
        if self.expires_at is None:
            return False
        return _now_utc() > self.expires_at

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
            expires_at=(datetime.fromisoformat(d["expires_at"]) if d.get("expires_at") else None),
        )


class Session:
    """
    Session interface for accessing session data.

    Provides a typed interface to session data with automatic
    persistence through the session store.

    Example:
        ```python
        # Simple dict-like access
        ctx.session.set("user_id", 123)
        user_id = ctx.session.get("user_id")

        # Dict-like operations
        ctx.session["key"] = "value"
        value = ctx.session["key"]
        if "key" in ctx.session:
            ctx.session.delete("key")
        ```
    """

    def __init__(
        self,
        session_data: SessionData | None = None,
        store: "SessionStore | None" = None,
    ):
        """
        Initialize the session.

        Args:
            session_data: The underlying session data
            store: Optional session store for persistence
        """
        self._data = session_data or SessionData()
        self._store = store
        self._modified = False

    @property
    def id(self) -> str:
        """Get session ID."""
        return self._data.id

    @property
    def session_id(self) -> str:
        """Get session ID (alias for compatibility)."""
        return self._data.id

    @property
    def created_at(self) -> datetime:
        """Get session creation time."""
        return self._data.created_at

    @property
    def updated_at(self) -> datetime:
        """Get session last update time."""
        return self._data.updated_at

    @property
    def is_modified(self) -> bool:
        """Check if session has been modified."""
        return self._modified

    @property
    def is_expired(self) -> bool:
        """Check if session has expired."""
        return self._data.is_expired()

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a value from the session.

        Args:
            key: The key to look up
            default: Value to return if key not found

        Returns:
            The value or default
        """
        return self._data.data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """
        Set a value in the session.

        Args:
            key: The key to set
            value: The value to store
        """
        self._data.data[key] = value
        self._data.updated_at = _now_utc()
        self._modified = True

    def delete(self, key: str) -> None:
        """
        Delete a value from the session.

        Args:
            key: The key to delete
        """
        if key in self._data.data:
            del self._data.data[key]
            self._data.updated_at = _now_utc()
            self._modified = True

    def clear(self) -> None:
        """Clear all session data."""
        self._data.data.clear()
        self._data.updated_at = _now_utc()
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

    def __delitem__(self, key: str) -> None:
        """Dict-like deletion."""
        self.delete(key)

    def keys(self) -> list[str]:
        """Get all session keys."""
        return list(self._data.data.keys())

    def values(self) -> list[Any]:
        """Get all session values."""
        return list(self._data.data.values())

    def items(self) -> list[tuple[str, Any]]:
        """Get all session items."""
        return list(self._data.data.items())

    def to_dict(self) -> dict[str, Any]:
        """Convert session data to dictionary."""
        return self._data.to_dict()

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
        """
        Set session expiry time.

        Args:
            seconds: Number of seconds until expiry
        """
        self._data.expires_at = _now_utc() + timedelta(seconds=seconds)
        self._modified = True

    def __repr__(self) -> str:
        """Return string representation."""
        return f"Session(id={self.id!r}, keys={self.keys()!r})"
        return self._data.copy()
