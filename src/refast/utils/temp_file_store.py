"""Temporary file storage for uploaded files."""

import asyncio
import time
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class FileInfo:
    """
    Metadata about a file stored in a :class:`TempFileStore`.

    Attributes:
        id: Unique file identifier (UUID).
        name: Original filename as provided by the uploader.
        size: File size in bytes.
        content_type: MIME type of the file.
        inline: When ``True`` the file is served with
            ``Content-Disposition: inline`` so browsers display it
            (images, video, PDF).  When ``False`` (default) it is served
            with ``Content-Disposition: attachment`` to force a download.
    """

    id: str
    name: str
    size: int
    content_type: str
    inline: bool = False
    _store: Any = field(default=None, repr=False, compare=False)

    async def read(self) -> bytes:
        """Read the file content from the store.

        Raises:
            RuntimeError: If the :class:`FileInfo` has no associated store.
            FileNotFoundError: If the file has expired or been deleted.
        """
        if self._store is None:
            raise RuntimeError("No store associated with this FileInfo")
        data = await self._store.get_file(self.id)
        if data is None:
            raise FileNotFoundError(f"File {self.id!r} not found or expired")
        return data

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serialisable dict (without internal store reference)."""
        return {
            "id": self.id,
            "name": self.name,
            "size": self.size,
            "content_type": self.content_type,
            "inline": self.inline,
        }


class TempFileStore(ABC):
    """
    Abstract base class for temporary file storage.

    Subclasses must implement :meth:`store_file`, :meth:`get_file`,
    :meth:`get_file_info`, and :meth:`delete_file`.

    Args:
        max_size_bytes: Maximum allowed size per file in bytes.
            ``None`` means no limit.
        ttl_seconds: How long files are kept before they expire.
    """

    def __init__(
        self,
        max_size_bytes: int | None = 10 * 1024 * 1024,
        ttl_seconds: int = 3600,
    ) -> None:
        self.max_size_bytes = max_size_bytes
        self.ttl_seconds = ttl_seconds

    def _validate_size(self, data: bytes) -> None:
        """Raise :exc:`ValueError` if *data* exceeds :attr:`max_size_bytes`."""
        if self.max_size_bytes is not None and len(data) > self.max_size_bytes:
            raise ValueError(
                f"File size {len(data)} bytes exceeds the limit of {self.max_size_bytes} bytes"
            )

    @abstractmethod
    async def store_file(
        self,
        data: bytes,
        filename: str,
        content_type: str = "application/octet-stream",
        inline: bool = False,
    ) -> FileInfo:
        """Store *data* and return a :class:`FileInfo` with a unique ID.

        Args:
            data: Raw file bytes.
            filename: Original filename.
            content_type: MIME type.
            inline: Serve inline (``True``) or as attachment (``False``).

        Raises:
            ValueError: If *data* exceeds :attr:`max_size_bytes`.
        """
        ...

    @abstractmethod
    async def get_file(self, file_id: str) -> bytes | None:
        """Return the raw bytes for *file_id*, or ``None`` if missing/expired."""
        ...

    @abstractmethod
    async def get_file_info(self, file_id: str) -> FileInfo | None:
        """Return metadata for *file_id*, or ``None`` if missing/expired."""
        ...

    @abstractmethod
    async def delete_file(self, file_id: str) -> None:
        """Delete the file identified by *file_id* (no-op if not found)."""
        ...


class MemoryFileStore(TempFileStore):
    """
    In-memory temporary file store.

    Files are stored in a plain Python dict. Suitable for most use cases
    where file sizes are reasonable (controlled by *max_size_bytes*).

    A background :mod:`asyncio` task cleans up expired entries automatically
    when the store is first used inside a running event loop.

    Args:
        max_size_bytes: Maximum allowed size per file. Defaults to 10 MiB.
        ttl_seconds: Time-to-live for stored files. Defaults to 3600 s.

    Example:
        ```python
        store = MemoryFileStore(max_size_bytes=5 * 1024 * 1024, ttl_seconds=600)
        ui = RefastApp(file_store=store)
        ```
    """

    def __init__(
        self,
        max_size_bytes: int | None = 10 * 1024 * 1024,
        ttl_seconds: int = 3600,
    ) -> None:
        super().__init__(max_size_bytes=max_size_bytes, ttl_seconds=ttl_seconds)
        # {file_id: (data, FileInfo, expires_at)}
        self._files: dict[str, tuple[bytes, FileInfo, float]] = {}
        self._cleanup_task: asyncio.Task[None] | None = None

    # ── Cleanup ────────────────────────────────────────────────────────────

    def _start_cleanup(self) -> None:
        """Ensure the background cleanup task is running."""
        try:
            loop = asyncio.get_running_loop()
            if self._cleanup_task is None or self._cleanup_task.done():
                self._cleanup_task = loop.create_task(self._cleanup_loop())
        except RuntimeError:
            pass  # No event loop (e.g. during tests with non-async code)

    async def _cleanup_loop(self) -> None:
        while True:
            interval = max(min(self.ttl_seconds / 2, 300), 1)
            await asyncio.sleep(interval)
            self._cleanup_expired()

    def _cleanup_expired(self) -> None:
        now = time.monotonic()
        expired = [fid for fid, (_, _, exp) in self._files.items() if exp <= now]
        for fid in expired:
            del self._files[fid]

    # ── TempFileStore interface ────────────────────────────────────────────

    async def store_file(
        self,
        data: bytes,
        filename: str,
        content_type: str = "application/octet-stream",
        inline: bool = False,
    ) -> FileInfo:
        self._validate_size(data)
        file_id = str(uuid.uuid4())
        info = FileInfo(
            id=file_id,
            name=filename,
            size=len(data),
            content_type=content_type,
            inline=inline,
            _store=self,
        )
        expires_at = time.monotonic() + self.ttl_seconds
        self._files[file_id] = (data, info, expires_at)
        self._start_cleanup()
        return info

    async def get_file(self, file_id: str) -> bytes | None:
        entry = self._files.get(file_id)
        if entry is None:
            return None
        data, _, expires_at = entry
        if time.monotonic() > expires_at:
            del self._files[file_id]
            return None
        return data

    async def get_file_info(self, file_id: str) -> FileInfo | None:
        entry = self._files.get(file_id)
        if entry is None:
            return None
        _, info, expires_at = entry
        if time.monotonic() > expires_at:
            del self._files[file_id]
            return None
        return info

    async def delete_file(self, file_id: str) -> None:
        self._files.pop(file_id, None)


class DiskFileStore(TempFileStore):
    """
    Disk-based temporary file store.

    Files are written to a temporary directory.  Suitable for large files
    where keeping them in memory is impractical.

    A background :mod:`asyncio` task cleans up expired files automatically.

    Args:
        max_size_bytes: Maximum allowed size per file. Defaults to 100 MiB.
        ttl_seconds: Time-to-live for stored files. Defaults to 3600 s.
        directory: Directory to store files in.  A new temporary directory
            under the system's temp location is created if omitted.

    Example:
        ```python
        store = DiskFileStore(
            max_size_bytes=500 * 1024 * 1024,
            directory="/var/tmp/refast_uploads",
        )
        ui = RefastApp(file_store=store)
        ```
    """

    def __init__(
        self,
        max_size_bytes: int | None = 100 * 1024 * 1024,
        ttl_seconds: int = 3600,
        directory: str | None = None,
    ) -> None:
        super().__init__(max_size_bytes=max_size_bytes, ttl_seconds=ttl_seconds)
        if directory is not None:
            self._directory = Path(directory)
        else:
            import tempfile

            self._directory = Path(tempfile.mkdtemp(prefix="refast_uploads_"))
        self._directory.mkdir(parents=True, exist_ok=True)
        # {file_id: (FileInfo, expires_at)}
        self._metadata: dict[str, tuple[FileInfo, float]] = {}
        self._cleanup_task: asyncio.Task[None] | None = None

    def _file_path(self, file_id: str) -> Path:
        return self._directory / file_id

    # ── Cleanup ────────────────────────────────────────────────────────────

    def _start_cleanup(self) -> None:
        try:
            loop = asyncio.get_running_loop()
            if self._cleanup_task is None or self._cleanup_task.done():
                self._cleanup_task = loop.create_task(self._cleanup_loop())
        except RuntimeError:
            pass

    async def _cleanup_loop(self) -> None:
        while True:
            interval = max(min(self.ttl_seconds / 2, 300), 1)
            await asyncio.sleep(interval)
            self._cleanup_expired()

    def _cleanup_expired(self) -> None:
        now = time.monotonic()
        expired = [fid for fid, (_, exp) in self._metadata.items() if exp <= now]
        for fid in expired:
            self._file_path(fid).unlink(missing_ok=True)
            del self._metadata[fid]

    # ── TempFileStore interface ────────────────────────────────────────────

    async def store_file(
        self,
        data: bytes,
        filename: str,
        content_type: str = "application/octet-stream",
        inline: bool = False,
    ) -> FileInfo:
        self._validate_size(data)
        file_id = str(uuid.uuid4())
        self._file_path(file_id).write_bytes(data)
        info = FileInfo(
            id=file_id,
            name=filename,
            size=len(data),
            content_type=content_type,
            inline=inline,
            _store=self,
        )
        expires_at = time.monotonic() + self.ttl_seconds
        self._metadata[file_id] = (info, expires_at)
        self._start_cleanup()
        return info

    async def get_file(self, file_id: str) -> bytes | None:
        entry = self._metadata.get(file_id)
        if entry is None:
            return None
        _, expires_at = entry
        if time.monotonic() > expires_at:
            self._file_path(file_id).unlink(missing_ok=True)
            del self._metadata[file_id]
            return None
        path = self._file_path(file_id)
        if not path.exists():
            self._metadata.pop(file_id, None)
            return None
        return path.read_bytes()

    async def get_file_info(self, file_id: str) -> FileInfo | None:
        entry = self._metadata.get(file_id)
        if entry is None:
            return None
        info, expires_at = entry
        if time.monotonic() > expires_at:
            self._file_path(file_id).unlink(missing_ok=True)
            del self._metadata[file_id]
            return None
        return info

    async def delete_file(self, file_id: str) -> None:
        self._file_path(file_id).unlink(missing_ok=True)
        self._metadata.pop(file_id, None)
