"""
Browser storage management for persistent state.

Provides access to browser's localStorage and sessionStorage from Python,
enabling state that persists across page refreshes and browser restarts.
"""

import asyncio
import json
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Protocol

if TYPE_CHECKING:
    from refast.context import Context


class Encoder(Protocol):
    """Protocol for value encoding/decoding."""

    def encode(self, value: Any) -> str:
        """Encode a value to string for storage."""
        ...

    def decode(self, data: str) -> Any:
        """Decode a string back to value."""
        ...


class JSONEncoder:
    """Default JSON encoder for storage values."""

    def encode(self, value: Any) -> str:
        """Encode value to JSON string."""
        return json.dumps(value)

    def decode(self, data: str) -> Any:
        """Decode JSON string to value."""
        return json.loads(data)


class BrowserStore(ABC):
    """
    Abstract base class for browser storage.

    Provides a dict-like interface to browser storage (localStorage/sessionStorage).
    Values are synced to the browser via WebSocket and persisted client-side.

    Example:
        ```python
        # Get a value with default
        theme = ctx.store.local.get("theme", "light")

        # Set a value
        ctx.store.local.set("theme", "dark")

        # Check if key exists
        if "user_prefs" in ctx.store.local:
            prefs = ctx.store.local.get("user_prefs")
        ```
    """

    def __init__(
        self,
        storage_type: str,
        ctx: "Context",
        encoder: Encoder | None = None,
        encrypt: bool = False,
    ):
        """
        Initialize the browser store.

        Args:
            storage_type: Either "local" or "session"
            ctx: The request context for WebSocket communication
            encoder: Custom encoder for serialization (default: JSONEncoder)
            encrypt: Whether to encrypt stored values (default: False)
        """
        self._storage_type = storage_type
        self._ctx = ctx
        self._encoder = encoder or JSONEncoder()
        self._encrypt = encrypt
        self._data: dict[str, Any] = {}
        self._pending_updates: list[dict[str, Any]] = []
        self._sync_scheduled = False

    @property
    def storage_type(self) -> str:
        """Return the storage type (local or session)."""
        return self._storage_type

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a value from storage.

        Args:
            key: The key to retrieve
            default: Default value if key doesn't exist

        Returns:
            The stored value or default

        Note:
            This returns the cached value. If JavaScript has modified
            localStorage directly, call `await ctx.store.sync()` first
            to refresh the cache from the browser.
        """
        return self._data.get(key, default)

    def get_all(self) -> dict[str, Any]:
        """
        Get all stored values.

        Returns:
            Dictionary of all stored key-value pairs
        """
        return self._data.copy()

    def set(self, key: str, value: Any) -> None:
        """
        Set a value in storage.

        The value is immediately available locally and will be
        synced to the browser on the next WebSocket message.

        Args:
            key: The key to set
            value: The value to store (must be JSON-serializable)
        """
        self._data[key] = value
        self._queue_update("set", key, value)

    def set_many(self, data: dict[str, Any]) -> None:
        """
        Set multiple values at once.

        Args:
            data: Dictionary of key-value pairs to set
        """
        self._data.update(data)
        for key, value in data.items():
            self._queue_update("set", key, value)

    def delete(self, key: str) -> None:
        """
        Delete a key from storage.

        Args:
            key: The key to delete
        """
        if key in self._data:
            del self._data[key]
        self._queue_update("delete", key)

    def clear(self) -> None:
        """Clear all values from storage."""
        self._data.clear()
        self._queue_update("clear", None)

    def __contains__(self, key: str) -> bool:
        """Check if key exists in storage."""
        return key in self._data

    def __getitem__(self, key: str) -> Any:
        """Get a value using bracket notation."""
        return self._data[key]

    def __setitem__(self, key: str, value: Any) -> None:
        """Set a value using bracket notation."""
        self.set(key, value)

    def __delitem__(self, key: str) -> None:
        """Delete a value using bracket notation."""
        self.delete(key)

    def keys(self) -> list[str]:
        """Return all keys in storage."""
        return list(self._data.keys())

    def values(self) -> list[Any]:
        """Return all values in storage."""
        return list(self._data.values())

    def items(self) -> list[tuple[str, Any]]:
        """Return all key-value pairs in storage."""
        return list(self._data.items())

    def _queue_update(self, operation: str, key: str | None, value: Any = None) -> None:
        """Queue an update and schedule automatic sync to browser."""
        update = {
            "storageType": self._storage_type,
            "operation": operation,
            "key": key,
            "encrypt": self._encrypt,
        }
        if value is not None:
            # Send the raw value - frontend will handle serialization
            # This avoids double-encoding strings
            update["value"] = value
        self._pending_updates.append(update)

        # Auto-schedule sync if not already scheduled
        self._schedule_sync()

    def _schedule_sync(self) -> None:
        """Schedule an automatic sync to the browser."""
        if self._sync_scheduled:
            return

        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            # No running event loop - sync will happen manually or after callback
            return

        self._sync_scheduled = True
        loop.call_soon(self._do_sync)

    def _do_sync(self) -> None:
        """Perform the actual sync by creating a task."""
        self._sync_scheduled = False
        try:
            loop = asyncio.get_running_loop()
            loop.create_task(self._ctx.sync_store())
        except RuntimeError:
            # No running event loop
            pass

    def _load_from_browser(self, data: dict[str, str]) -> None:
        """
        Load data received from browser storage.

        Called internally when the browser sends its storage state.

        Args:
            data: Dictionary of key-value pairs from browser
        """
        self._data.clear()
        for key, value in data.items():
            # Try to parse as JSON for complex types
            # If it fails, store the raw string value
            try:
                self._data[key] = json.loads(value)
            except (json.JSONDecodeError, TypeError):
                # Not valid JSON, store as plain string
                self._data[key] = value

    def _get_pending_updates(self) -> list[dict[str, Any]]:
        """Get and clear pending updates."""
        updates = self._pending_updates.copy()
        self._pending_updates.clear()
        return updates

    @abstractmethod
    def _get_storage_key_prefix(self) -> str:
        """Get the prefix for storage keys."""
        ...


class LocalStore(BrowserStore):
    """
    Access to browser's localStorage.

    Data persists across page refreshes and browser restarts.
    Shared across all tabs/windows of the same origin.

    Example:
        ```python
        @ui.page("/settings")
        def settings(ctx: Context):
            # Load user's theme preference
            theme = ctx.store.local.get("theme", "light")
            return SettingsPage(theme=theme)

        async def save_theme(ctx: Context, theme: str):
            # Save theme - persists even after browser restart
            ctx.store.local.set("theme", theme)
            await ctx.refresh()
        ```
    """

    def __init__(
        self,
        ctx: "Context",
        encoder: Encoder | None = None,
        encrypt: bool = False,
    ):
        super().__init__("local", ctx, encoder, encrypt)

    def _get_storage_key_prefix(self) -> str:
        return "refast:local:"


class SessionStore(BrowserStore):
    """
    Access to browser's sessionStorage.

    Data persists across page refreshes but NOT across browser restarts.
    Each tab/window has its own sessionStorage.

    Example:
        ```python
        @ui.page("/wizard")
        def wizard(ctx: Context):
            # Load current wizard step (persists across refresh)
            step = ctx.store.session.get("wizard_step", 1)
            return WizardPage(step=step)

        async def next_step(ctx: Context):
            # Save step - persists until tab is closed
            step = ctx.store.session.get("wizard_step", 1)
            ctx.store.session.set("wizard_step", step + 1)
            await ctx.refresh()
        ```
    """

    def __init__(
        self,
        ctx: "Context",
        encoder: Encoder | None = None,
        encrypt: bool = False,
    ):
        super().__init__("session", ctx, encoder, encrypt)

    def _get_storage_key_prefix(self) -> str:
        return "refast:session:"


class Store:
    """
    Container for browser storage access.

    Provides access to both localStorage and sessionStorage via
    `ctx.store.local` and `ctx.store.session`.

    Example:
        ```python
        # localStorage - persists across browser restarts
        ctx.store.local.set("user_id", 123)

        # sessionStorage - persists until tab is closed
        ctx.store.session.set("temp_data", {"key": "value"})

        # Sync from browser to get JS-modified values
        await ctx.store.sync()
        value = ctx.store.local.get("js_set_key")
        ```
    """

    def __init__(
        self,
        ctx: "Context",
        encoder: Encoder | None = None,
        encrypt: bool = False,
    ):
        """
        Initialize the store container.

        Args:
            ctx: The request context
            encoder: Custom encoder for serialization
            encrypt: Whether to encrypt stored values
        """
        self._ctx = ctx
        self._local = LocalStore(ctx, encoder, encrypt)
        self._session = SessionStore(ctx, encoder, encrypt)

    @property
    def local(self) -> LocalStore:
        """
        Access localStorage.

        Returns:
            LocalStore instance for localStorage access
        """
        return self._local

    @property
    def session(self) -> SessionStore:
        """
        Access sessionStorage.

        Returns:
            SessionStore instance for sessionStorage access
        """
        return self._session

    async def sync(self) -> None:
        """
        Sync the store cache from the browser.

        Call this method when you need to read values that JavaScript
        may have modified directly in localStorage or sessionStorage.
        After calling sync(), subsequent get() calls will return the
        latest browser values.

        Example:
            ```python
            async def read_js_value(ctx: Context):
                # JS may have set this value directly
                await ctx.store.sync()

                # Now get() returns the fresh browser value
                value = ctx.store.local.get("js_set_key")
                print(f"Value from browser: {value}")
            ```
        """
        await self._ctx._sync_store_from_browser()

    def _load_from_browser(self, data: dict[str, dict[str, str]]) -> None:
        """
        Load data from browser for both storage types.

        Args:
            data: Dictionary with "local" and "session" keys
        """
        if "local" in data:
            self._local._load_from_browser(data["local"])
        if "session" in data:
            self._session._load_from_browser(data["session"])

    def _get_all_pending_updates(self) -> list[dict[str, Any]]:
        """Get pending updates from both stores."""
        return self._local._get_pending_updates() + self._session._get_pending_updates()
