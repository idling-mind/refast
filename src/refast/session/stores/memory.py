"""In-memory session store."""

import asyncio
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any

from refast.session.stores.base import SessionStore


def _now_utc() -> datetime:
    """Get current UTC time."""
    return datetime.now(UTC)


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

    Attributes:
        default_ttl: Default time-to-live in seconds
        cleanup_interval: Seconds between cleanup runs
    """

    def __init__(
        self,
        default_ttl: int = 3600,
        cleanup_interval: int = 300,
    ):
        """
        Initialize the memory store.

        Args:
            default_ttl: Default time-to-live in seconds
            cleanup_interval: Seconds between cleanup runs
        """
        self._store: dict[str, MemoryEntry] = {}
        self._default_ttl = default_ttl
        self._cleanup_interval = cleanup_interval
        self._cleanup_task: asyncio.Task[None] | None = None
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
        """
        Retrieve session data.

        Args:
            session_id: The session identifier

        Returns:
            Session data or None if not found/expired
        """
        async with self._lock:
            entry = self._store.get(session_id)
            if entry is None:
                return None

            # Check expiration
            if _now_utc() > entry.expires_at:
                del self._store[session_id]
                return None

            return entry.data

    async def set(
        self,
        session_id: str,
        data: dict[str, Any],
        ttl: int | None = None,
    ) -> None:
        """
        Store session data.

        Args:
            session_id: The session identifier
            data: The session data
            ttl: Time-to-live in seconds (uses default if not specified)
        """
        if ttl is None:
            ttl = self._default_ttl

        expires_at = _now_utc() + timedelta(seconds=ttl)

        async with self._lock:
            self._store[session_id] = MemoryEntry(
                data=data,
                expires_at=expires_at,
            )

    async def delete(self, session_id: str) -> None:
        """
        Delete a session.

        Args:
            session_id: The session identifier
        """
        async with self._lock:
            self._store.pop(session_id, None)

    async def exists(self, session_id: str) -> bool:
        """
        Check if session exists.

        Args:
            session_id: The session identifier

        Returns:
            True if session exists and is not expired
        """
        data = await self.get(session_id)
        return data is not None

    async def clear_expired(self) -> int:
        """
        Clear expired sessions.

        Returns:
            Number of sessions cleared
        """
        now = _now_utc()
        count = 0

        async with self._lock:
            expired_ids = [
                sid for sid, entry in self._store.items() if now > entry.expires_at
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
                await self.clear_expired()
            except asyncio.CancelledError:
                break
            except Exception:
                pass  # Log error in production
