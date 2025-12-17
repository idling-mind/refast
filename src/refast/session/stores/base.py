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

            async def set(
                self, session_id: str, data: dict, ttl: int = 3600
            ) -> None:
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

    @abstractmethod
    async def delete(self, session_id: str) -> None:
        """
        Delete a session.

        Args:
            session_id: The session identifier
        """

    @abstractmethod
    async def exists(self, session_id: str) -> bool:
        """
        Check if a session exists.

        Args:
            session_id: The session identifier

        Returns:
            True if session exists
        """

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
