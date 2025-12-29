"""Tests for MemorySessionStore."""

import asyncio

import pytest

from refast.session.stores.memory import MemorySessionStore


class TestMemorySessionStore:
    """Tests for MemorySessionStore class."""

    @pytest.fixture
    def store(self):
        """Create a memory store fixture."""
        return MemorySessionStore(default_ttl=60)

    @pytest.mark.asyncio
    async def test_set_and_get(self, store):
        """Test setting and getting session data."""
        await store.set("session-1", {"key": "value"})
        data = await store.get("session-1")
        assert data is not None
        assert data["key"] == "value"

    @pytest.mark.asyncio
    async def test_get_nonexistent(self, store):
        """Test getting nonexistent session."""
        data = await store.get("nonexistent")
        assert data is None

    @pytest.mark.asyncio
    async def test_delete(self, store):
        """Test deleting session."""
        await store.set("session-1", {"key": "value"})
        await store.delete("session-1")
        data = await store.get("session-1")
        assert data is None

    @pytest.mark.asyncio
    async def test_delete_nonexistent(self, store):
        """Test deleting nonexistent session."""
        await store.delete("nonexistent")  # Should not raise

    @pytest.mark.asyncio
    async def test_exists(self, store):
        """Test checking session existence."""
        await store.set("session-1", {})
        assert await store.exists("session-1")
        assert not await store.exists("nonexistent")

    @pytest.mark.asyncio
    async def test_expired_session(self, store):
        """Test expired session is not returned."""
        await store.set("session-1", {"key": "value"}, ttl=0)
        await asyncio.sleep(0.01)
        data = await store.get("session-1")
        assert data is None

    @pytest.mark.asyncio
    async def test_unexpired_session(self, store):
        """Test unexpired session is returned."""
        await store.set("session-1", {"key": "value"}, ttl=3600)
        data = await store.get("session-1")
        assert data is not None

    @pytest.mark.asyncio
    async def test_clear_expired(self, store):
        """Test clearing expired sessions."""
        await store.set("session-1", {}, ttl=0)
        await store.set("session-2", {}, ttl=3600)

        await asyncio.sleep(0.01)

        count = await store.clear_expired()
        assert count == 1
        assert not await store.exists("session-1")
        assert await store.exists("session-2")

    @pytest.mark.asyncio
    async def test_clear_all(self, store):
        """Test clearing all sessions."""
        await store.set("session-1", {})
        await store.set("session-2", {})
        await store.clear_all()
        assert store.session_count() == 0

    @pytest.mark.asyncio
    async def test_session_count(self, store):
        """Test getting session count."""
        assert store.session_count() == 0
        await store.set("session-1", {})
        assert store.session_count() == 1
        await store.set("session-2", {})
        assert store.session_count() == 2

    @pytest.mark.asyncio
    async def test_touch(self, store):
        """Test touching session to extend TTL."""
        await store.set("session-1", {"key": "value"}, ttl=1)
        result = await store.touch("session-1", ttl=3600)
        assert result is True

    @pytest.mark.asyncio
    async def test_touch_nonexistent(self, store):
        """Test touching nonexistent session."""
        result = await store.touch("nonexistent")
        assert result is False

    @pytest.mark.asyncio
    async def test_default_ttl(self):
        """Test default TTL is used."""
        store = MemorySessionStore(default_ttl=1)
        await store.set("session-1", {})

        # Should still exist immediately
        assert await store.exists("session-1")

    @pytest.mark.asyncio
    async def test_overwrite_session(self, store):
        """Test overwriting existing session."""
        await store.set("session-1", {"v": 1})
        await store.set("session-1", {"v": 2})
        data = await store.get("session-1")
        assert data["v"] == 2

    @pytest.mark.asyncio
    async def test_concurrent_access(self, store):
        """Test concurrent access is safe."""

        async def set_session(i):
            await store.set(f"session-{i}", {"value": i})

        await asyncio.gather(*[set_session(i) for i in range(100)])
        assert store.session_count() == 100

    @pytest.mark.asyncio
    async def test_start_stop_cleanup(self, store):
        """Test starting and stopping cleanup task."""
        await store.start_cleanup()
        assert store._cleanup_task is not None

        await store.stop_cleanup()
        assert store._cleanup_task is None
