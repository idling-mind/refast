"""Unit tests for TempFileStore implementations."""

import time

import pytest

from refast.utils.temp_file_store import DiskFileStore, FileInfo, MemoryFileStore

# ─── FileInfo ─────────────────────────────────────────────────────────────────


class TestFileInfo:
    def test_to_dict_contains_all_fields(self):
        info = FileInfo(id="abc", name="test.txt", size=42, content_type="text/plain")
        d = info.to_dict()
        assert d["id"] == "abc"
        assert d["name"] == "test.txt"
        assert d["size"] == 42
        assert d["content_type"] == "text/plain"
        assert d["inline"] is False

    def test_to_dict_no_store_reference(self):
        info = FileInfo(id="x", name="f", size=0, content_type="text/plain")
        d = info.to_dict()
        assert "_store" not in d

    def test_inline_flag_default_false(self):
        info = FileInfo(id="y", name="img.png", size=100, content_type="image/png")
        assert info.inline is False

    def test_inline_flag_true(self):
        info = FileInfo(id="y", name="img.png", size=100, content_type="image/png", inline=True)
        d = info.to_dict()
        assert d["inline"] is True

    @pytest.mark.asyncio
    async def test_read_raises_without_store(self):
        info = FileInfo(id="x", name="f", size=0, content_type="text/plain")
        with pytest.raises(RuntimeError, match="No store"):
            await info.read()

    @pytest.mark.asyncio
    async def test_read_with_store(self):
        store = MemoryFileStore()
        info = await store.store_file(b"hello", "hi.txt", "text/plain")
        data = await info.read()
        assert data == b"hello"

    @pytest.mark.asyncio
    async def test_read_raises_when_expired(self):
        store = MemoryFileStore(ttl_seconds=1)
        info = await store.store_file(b"data", "f.bin", "application/octet-stream")
        # Manually expire by manipulating the stored expiry
        fid = info.id
        data, meta, _ = store._files[fid]
        store._files[fid] = (data, meta, time.monotonic() - 1)
        with pytest.raises(FileNotFoundError):
            await info.read()


# ─── MemoryFileStore ──────────────────────────────────────────────────────────


class TestMemoryFileStore:
    @pytest.mark.asyncio
    async def test_store_and_retrieve(self):
        store = MemoryFileStore()
        info = await store.store_file(b"content", "file.txt", "text/plain")
        assert info.name == "file.txt"
        assert info.size == 7
        assert info.content_type == "text/plain"
        data = await store.get_file(info.id)
        assert data == b"content"

    @pytest.mark.asyncio
    async def test_get_file_returns_none_for_unknown(self):
        store = MemoryFileStore()
        result = await store.get_file("nonexistent-id")
        assert result is None

    @pytest.mark.asyncio
    async def test_get_file_info_returns_none_for_unknown(self):
        store = MemoryFileStore()
        result = await store.get_file_info("nonexistent-id")
        assert result is None

    @pytest.mark.asyncio
    async def test_delete_file(self):
        store = MemoryFileStore()
        info = await store.store_file(b"bye", "bye.bin", "application/octet-stream")
        await store.delete_file(info.id)
        assert await store.get_file(info.id) is None

    @pytest.mark.asyncio
    async def test_delete_nonexistent_is_noop(self):
        store = MemoryFileStore()
        await store.delete_file("ghost")  # should not raise

    @pytest.mark.asyncio
    async def test_size_limit_enforced(self):
        store = MemoryFileStore(max_size_bytes=10)
        with pytest.raises(ValueError, match="exceeds"):
            await store.store_file(b"x" * 11, "big.bin", "application/octet-stream")

    @pytest.mark.asyncio
    async def test_size_limit_none_allows_any_size(self):
        store = MemoryFileStore(max_size_bytes=None)
        data = b"x" * 10_000
        info = await store.store_file(data, "large.bin", "application/octet-stream")
        assert info.size == 10_000

    @pytest.mark.asyncio
    async def test_ttl_expiry(self):
        store = MemoryFileStore(ttl_seconds=1)
        info = await store.store_file(b"temp", "temp.txt", "text/plain")
        fid = info.id
        # Manually expire
        data, meta, _ = store._files[fid]
        store._files[fid] = (data, meta, time.monotonic() - 1)
        assert await store.get_file(fid) is None
        assert fid not in store._files  # cleaned up

    @pytest.mark.asyncio
    async def test_get_file_info_after_expiry(self):
        store = MemoryFileStore(ttl_seconds=1)
        info = await store.store_file(b"x", "x.bin", "application/octet-stream")
        fid = info.id
        data, meta, _ = store._files[fid]
        store._files[fid] = (data, meta, time.monotonic() - 1)
        assert await store.get_file_info(fid) is None

    @pytest.mark.asyncio
    async def test_inline_flag_stored(self):
        store = MemoryFileStore()
        info = await store.store_file(b"img", "img.png", "image/png", inline=True)
        assert info.inline is True
        retrieved = await store.get_file_info(info.id)
        assert retrieved is not None
        assert retrieved.inline is True

    @pytest.mark.asyncio
    async def test_multiple_files_independent(self):
        store = MemoryFileStore()
        info_a = await store.store_file(b"aaa", "a.txt", "text/plain")
        info_b = await store.store_file(b"bbb", "b.txt", "text/plain")
        assert await store.get_file(info_a.id) == b"aaa"
        assert await store.get_file(info_b.id) == b"bbb"

    @pytest.mark.asyncio
    async def test_cleanup_expired_removes_entries(self):
        store = MemoryFileStore(ttl_seconds=10)
        info = await store.store_file(b"x", "x.bin", "application/octet-stream")
        fid = info.id
        data, meta, _ = store._files[fid]
        store._files[fid] = (data, meta, time.monotonic() - 1)
        store._cleanup_expired()
        assert fid not in store._files


# ─── DiskFileStore ────────────────────────────────────────────────────────────


class TestDiskFileStore:
    @pytest.mark.asyncio
    async def test_store_and_retrieve(self, tmp_path):
        store = DiskFileStore(directory=str(tmp_path))
        info = await store.store_file(b"disk content", "disk.txt", "text/plain")
        assert info.name == "disk.txt"
        assert info.size == 12
        data = await store.get_file(info.id)
        assert data == b"disk content"

    @pytest.mark.asyncio
    async def test_file_written_to_disk(self, tmp_path):
        store = DiskFileStore(directory=str(tmp_path))
        info = await store.store_file(b"written", "written.bin", "application/octet-stream")
        assert (tmp_path / info.id).exists()

    @pytest.mark.asyncio
    async def test_delete_removes_file(self, tmp_path):
        store = DiskFileStore(directory=str(tmp_path))
        info = await store.store_file(b"del", "del.bin", "application/octet-stream")
        path = tmp_path / info.id
        assert path.exists()
        await store.delete_file(info.id)
        assert not path.exists()
        assert await store.get_file(info.id) is None

    @pytest.mark.asyncio
    async def test_get_file_returns_none_for_unknown(self, tmp_path):
        store = DiskFileStore(directory=str(tmp_path))
        assert await store.get_file("no-such-id") is None

    @pytest.mark.asyncio
    async def test_size_limit_enforced(self, tmp_path):
        store = DiskFileStore(max_size_bytes=5, directory=str(tmp_path))
        with pytest.raises(ValueError, match="exceeds"):
            await store.store_file(b"toolarge", "big.bin", "application/octet-stream")

    @pytest.mark.asyncio
    async def test_ttl_expiry(self, tmp_path):
        store = DiskFileStore(ttl_seconds=1, directory=str(tmp_path))
        info = await store.store_file(b"ttl", "ttl.bin", "application/octet-stream")
        fid = info.id
        meta, _ = store._metadata[fid]
        store._metadata[fid] = (meta, time.monotonic() - 1)
        assert await store.get_file(fid) is None

    @pytest.mark.asyncio
    async def test_cleanup_removes_disk_file(self, tmp_path):
        store = DiskFileStore(directory=str(tmp_path))
        info = await store.store_file(b"clean", "clean.bin", "application/octet-stream")
        fid = info.id
        meta, _ = store._metadata[fid]
        store._metadata[fid] = (meta, time.monotonic() - 1)
        store._cleanup_expired()
        assert not (tmp_path / fid).exists()
        assert fid not in store._metadata

    @pytest.mark.asyncio
    async def test_get_file_info(self, tmp_path):
        store = DiskFileStore(directory=str(tmp_path))
        info = await store.store_file(b"meta", "meta.bin", "application/octet-stream")
        retrieved = await store.get_file_info(info.id)
        assert retrieved is not None
        assert retrieved.name == "meta.bin"
        assert retrieved.size == 4

    @pytest.mark.asyncio
    async def test_inline_flag_stored(self, tmp_path):
        store = DiskFileStore(directory=str(tmp_path))
        info = await store.store_file(b"img", "img.png", "image/png", inline=True)
        retrieved = await store.get_file_info(info.id)
        assert retrieved is not None
        assert retrieved.inline is True

    @pytest.mark.asyncio
    async def test_creates_directory_if_missing(self, tmp_path):
        new_dir = tmp_path / "sub" / "store"
        store = DiskFileStore(directory=str(new_dir))
        assert new_dir.exists()
        info = await store.store_file(b"x", "x.bin", "application/octet-stream")
        assert info.id in store._metadata
