"""Redis session store."""

import json
from typing import Any

from refast.session.stores.base import SessionStore

try:
    import redis.asyncio as redis

    REDIS_AVAILABLE = True
except ImportError:
    redis = None  # type: ignore[assignment]
    REDIS_AVAILABLE = False


class RedisSessionStore(SessionStore):
    """
    Redis-backed session store.

    Suitable for production with multiple workers.
    Requires the `redis` extra: pip install refast[redis]

    Example:
        ```python
        store = RedisSessionStore(
            redis_url="redis://localhost:6379/0",
            prefix="refast:session:",
        )

        # Or with existing Redis client
        redis_client = redis.from_url("redis://localhost")
        store = RedisSessionStore(client=redis_client)
        ```

    Attributes:
        prefix: Key prefix for session keys in Redis
        default_ttl: Default time-to-live in seconds
    """

    def __init__(
        self,
        redis_url: str | None = None,
        client: Any = None,
        prefix: str = "refast:session:",
        default_ttl: int = 3600,
    ):
        """
        Initialize the Redis store.

        Args:
            redis_url: Redis connection URL
            client: Existing Redis client instance
            prefix: Key prefix for session keys
            default_ttl: Default time-to-live in seconds

        Raises:
            ImportError: If redis is not installed
            ValueError: If neither redis_url nor client is provided
        """
        if not REDIS_AVAILABLE:
            raise ImportError("Redis is not installed. Install with: pip install refast[redis]")

        self._prefix = prefix
        self._default_ttl = default_ttl

        if client:
            self._client = client
            self._owned_client = False
        elif redis_url:
            self._client = redis.from_url(redis_url)  # type: ignore[union-attr]
            self._owned_client = True
        else:
            raise ValueError("Either redis_url or client must be provided")

    def _key(self, session_id: str) -> str:
        """
        Generate the Redis key for a session.

        Args:
            session_id: The session identifier

        Returns:
            The full Redis key
        """
        return f"{self._prefix}{session_id}"

    async def get(self, session_id: str) -> dict[str, Any] | None:
        """
        Retrieve session data from Redis.

        Args:
            session_id: The session identifier

        Returns:
            Session data or None if not found
        """
        data = await self._client.get(self._key(session_id))
        if data is None:
            return None
        return json.loads(data)

    async def set(
        self,
        session_id: str,
        data: dict[str, Any],
        ttl: int | None = None,
    ) -> None:
        """
        Store session data in Redis.

        Args:
            session_id: The session identifier
            data: The session data
            ttl: Time-to-live in seconds
        """
        if ttl is None:
            ttl = self._default_ttl

        await self._client.setex(
            self._key(session_id),
            ttl,
            json.dumps(data),
        )

    async def delete(self, session_id: str) -> None:
        """
        Delete a session from Redis.

        Args:
            session_id: The session identifier
        """
        await self._client.delete(self._key(session_id))

    async def exists(self, session_id: str) -> bool:
        """
        Check if session exists in Redis.

        Args:
            session_id: The session identifier

        Returns:
            True if session exists
        """
        result = await self._client.exists(self._key(session_id))
        return result > 0

    async def touch(self, session_id: str, ttl: int | None = None) -> bool:
        """
        Extend session TTL.

        Args:
            session_id: The session identifier
            ttl: New time-to-live in seconds

        Returns:
            True if session was touched
        """
        if ttl is None:
            ttl = self._default_ttl

        result = await self._client.expire(self._key(session_id), ttl)
        return result > 0

    async def close(self) -> None:
        """Close the Redis connection if owned."""
        if self._owned_client:
            await self._client.close()
