"""Unit tests for browser storage management."""

import json

from refast.store import JSONEncoder, LocalStore, SessionStore, Store


class MockContext:
    """Mock context for testing."""

    def __init__(self):
        self._websocket = None


class TestJSONEncoder:
    """Tests for JSONEncoder class."""

    def test_encode_string(self):
        """Test encoding a string value."""
        encoder = JSONEncoder()
        result = encoder.encode("hello")
        assert result == '"hello"'

    def test_encode_number(self):
        """Test encoding a number value."""
        encoder = JSONEncoder()
        result = encoder.encode(42)
        assert result == "42"

    def test_encode_dict(self):
        """Test encoding a dictionary."""
        encoder = JSONEncoder()
        result = encoder.encode({"key": "value", "num": 123})
        parsed = json.loads(result)
        assert parsed == {"key": "value", "num": 123}

    def test_encode_list(self):
        """Test encoding a list."""
        encoder = JSONEncoder()
        result = encoder.encode([1, 2, 3, "four"])
        assert json.loads(result) == [1, 2, 3, "four"]

    def test_encode_nested(self):
        """Test encoding nested structures."""
        encoder = JSONEncoder()
        data = {"users": [{"name": "Alice"}, {"name": "Bob"}], "count": 2}
        result = encoder.encode(data)
        assert json.loads(result) == data

    def test_decode_string(self):
        """Test decoding a string value."""
        encoder = JSONEncoder()
        result = encoder.decode('"hello"')
        assert result == "hello"

    def test_decode_number(self):
        """Test decoding a number value."""
        encoder = JSONEncoder()
        result = encoder.decode("42")
        assert result == 42

    def test_decode_dict(self):
        """Test decoding a dictionary."""
        encoder = JSONEncoder()
        result = encoder.decode('{"key": "value"}')
        assert result == {"key": "value"}

    def test_decode_list(self):
        """Test decoding a list."""
        encoder = JSONEncoder()
        result = encoder.decode("[1, 2, 3]")
        assert result == [1, 2, 3]


class TestLocalStore:
    """Tests for LocalStore class."""

    def test_storage_type(self):
        """Test that storage type is 'local'."""
        ctx = MockContext()
        store = LocalStore(ctx)
        assert store.storage_type == "local"

    def test_get_storage_key_prefix(self):
        """Test the storage key prefix."""
        ctx = MockContext()
        store = LocalStore(ctx)
        assert store._get_storage_key_prefix() == "refast:local:"

    def test_set_and_get(self):
        """Test setting and getting a value."""
        ctx = MockContext()
        store = LocalStore(ctx)
        store.set("key", "value")
        assert store.get("key") == "value"

    def test_get_default(self):
        """Test getting a non-existent key with default."""
        ctx = MockContext()
        store = LocalStore(ctx)
        assert store.get("missing", "default") == "default"

    def test_get_default_none(self):
        """Test getting a non-existent key without default."""
        ctx = MockContext()
        store = LocalStore(ctx)
        assert store.get("missing") is None

    def test_set_many(self):
        """Test setting multiple values at once."""
        ctx = MockContext()
        store = LocalStore(ctx)
        store.set_many({"a": 1, "b": 2, "c": 3})
        assert store.get("a") == 1
        assert store.get("b") == 2
        assert store.get("c") == 3

    def test_delete(self):
        """Test deleting a key."""
        ctx = MockContext()
        store = LocalStore(ctx)
        store.set("key", "value")
        store.delete("key")
        assert store.get("key") is None

    def test_delete_nonexistent(self):
        """Test deleting a non-existent key doesn't raise."""
        ctx = MockContext()
        store = LocalStore(ctx)
        store.delete("missing")  # Should not raise

    def test_clear(self):
        """Test clearing all values."""
        ctx = MockContext()
        store = LocalStore(ctx)
        store.set_many({"a": 1, "b": 2})
        store.clear()
        assert store.get("a") is None
        assert store.get("b") is None

    def test_contains(self):
        """Test __contains__ method."""
        ctx = MockContext()
        store = LocalStore(ctx)
        store.set("exists", True)
        assert "exists" in store
        assert "missing" not in store

    def test_getitem(self):
        """Test bracket notation for getting."""
        ctx = MockContext()
        store = LocalStore(ctx)
        store.set("key", "value")
        assert store["key"] == "value"

    def test_setitem(self):
        """Test bracket notation for setting."""
        ctx = MockContext()
        store = LocalStore(ctx)
        store["key"] = "value"
        assert store.get("key") == "value"

    def test_delitem(self):
        """Test bracket notation for deleting."""
        ctx = MockContext()
        store = LocalStore(ctx)
        store["key"] = "value"
        del store["key"]
        assert "key" not in store

    def test_keys(self):
        """Test getting all keys."""
        ctx = MockContext()
        store = LocalStore(ctx)
        store.set_many({"a": 1, "b": 2, "c": 3})
        assert sorted(store.keys()) == ["a", "b", "c"]

    def test_values(self):
        """Test getting all values."""
        ctx = MockContext()
        store = LocalStore(ctx)
        store.set_many({"a": 1, "b": 2, "c": 3})
        assert sorted(store.values()) == [1, 2, 3]

    def test_items(self):
        """Test getting all items."""
        ctx = MockContext()
        store = LocalStore(ctx)
        store.set_many({"a": 1, "b": 2})
        items = dict(store.items())
        assert items == {"a": 1, "b": 2}

    def test_get_all(self):
        """Test getting all data."""
        ctx = MockContext()
        store = LocalStore(ctx)
        store.set_many({"a": 1, "b": 2})
        assert store.get_all() == {"a": 1, "b": 2}

    def test_get_all_returns_copy(self):
        """Test that get_all returns a copy."""
        ctx = MockContext()
        store = LocalStore(ctx)
        store.set("key", "value")
        data = store.get_all()
        data["key"] = "modified"
        assert store.get("key") == "value"


class TestSessionStore:
    """Tests for SessionStore class."""

    def test_storage_type(self):
        """Test that storage type is 'session'."""
        ctx = MockContext()
        store = SessionStore(ctx)
        assert store.storage_type == "session"

    def test_get_storage_key_prefix(self):
        """Test the storage key prefix."""
        ctx = MockContext()
        store = SessionStore(ctx)
        assert store._get_storage_key_prefix() == "refast:session:"

    def test_basic_operations(self):
        """Test basic set/get operations."""
        ctx = MockContext()
        store = SessionStore(ctx)
        store.set("wizard_step", 3)
        assert store.get("wizard_step") == 3


class TestStore:
    """Tests for Store container class."""

    def test_local_property(self):
        """Test access to local storage."""
        ctx = MockContext()
        store = Store(ctx)
        assert isinstance(store.local, LocalStore)
        assert store.local.storage_type == "local"

    def test_session_property(self):
        """Test access to session storage."""
        ctx = MockContext()
        store = Store(ctx)
        assert isinstance(store.session, SessionStore)
        assert store.session.storage_type == "session"

    def test_local_and_session_independent(self):
        """Test that local and session storage are independent."""
        ctx = MockContext()
        store = Store(ctx)
        store.local.set("key", "local_value")
        store.session.set("key", "session_value")
        assert store.local.get("key") == "local_value"
        assert store.session.get("key") == "session_value"

    def test_load_from_browser(self):
        """Test loading data from browser storage."""
        ctx = MockContext()
        store = Store(ctx)
        store._load_from_browser(
            {
                "local": {
                    "theme": "dark",  # Plain string
                    "count": "42",  # JSON number as string
                },
                "session": {
                    "step": "3",
                },
            }
        )
        assert store.local.get("theme") == "dark"
        assert store.local.get("count") == 42
        assert store.session.get("step") == 3

    def test_load_from_browser_partial(self):
        """Test loading with only one storage type."""
        ctx = MockContext()
        store = Store(ctx)
        store._load_from_browser({"local": {"key": "value"}})
        assert store.local.get("key") == "value"
        assert store.session.get("key") is None


class TestPendingUpdates:
    """Tests for pending update queue."""

    def test_set_queues_update(self):
        """Test that set() queues an update."""
        ctx = MockContext()
        store = LocalStore(ctx)
        store.set("key", "value")
        updates = store._get_pending_updates()
        assert len(updates) == 1
        assert updates[0]["storageType"] == "local"
        assert updates[0]["operation"] == "set"
        assert updates[0]["key"] == "key"
        assert updates[0]["value"] == "value"  # Raw value, not JSON-encoded

    def test_delete_queues_update(self):
        """Test that delete() queues an update."""
        ctx = MockContext()
        store = LocalStore(ctx)
        store.delete("key")
        updates = store._get_pending_updates()
        assert len(updates) == 1
        assert updates[0]["operation"] == "delete"
        assert updates[0]["key"] == "key"

    def test_clear_queues_update(self):
        """Test that clear() queues an update."""
        ctx = MockContext()
        store = LocalStore(ctx)
        store.clear()
        updates = store._get_pending_updates()
        assert len(updates) == 1
        assert updates[0]["operation"] == "clear"
        assert updates[0]["key"] is None

    def test_set_many_queues_multiple_updates(self):
        """Test that set_many() queues multiple updates."""
        ctx = MockContext()
        store = LocalStore(ctx)
        store.set_many({"a": 1, "b": 2})
        updates = store._get_pending_updates()
        assert len(updates) == 2

    def test_get_pending_updates_clears_queue(self):
        """Test that getting updates clears the queue."""
        ctx = MockContext()
        store = LocalStore(ctx)
        store.set("key", "value")
        store._get_pending_updates()
        updates = store._get_pending_updates()
        assert len(updates) == 0

    def test_store_get_all_pending_updates(self):
        """Test getting updates from both stores."""
        ctx = MockContext()
        store = Store(ctx)
        store.local.set("local_key", "value")
        store.session.set("session_key", "value")
        updates = store._get_all_pending_updates()
        assert len(updates) == 2
        storage_types = {u["storageType"] for u in updates}
        assert storage_types == {"local", "session"}


class TestLoadFromBrowser:
    """Tests for loading data from browser storage."""

    def test_load_replaces_existing_data(self):
        """Test that loading replaces existing data."""
        ctx = MockContext()
        store = LocalStore(ctx)
        store.set("old", "data")
        store._load_from_browser({"new": "data"})
        assert store.get("old") is None
        assert store.get("new") == "data"

    def test_load_handles_invalid_json(self):
        """Test that invalid JSON is stored as plain string."""
        ctx = MockContext()
        store = LocalStore(ctx)
        store._load_from_browser({"key": "not valid json"})
        assert store.get("key") == "not valid json"

    def test_load_handles_nested_data(self):
        """Test loading complex nested data."""
        ctx = MockContext()
        store = LocalStore(ctx)
        data = {"user": {"name": "Alice", "prefs": {"theme": "dark"}}}
        # Browser sends JSON-stringified objects
        store._load_from_browser({"user": json.dumps(data["user"])})
        assert store.get("user") == data["user"]


class TestEncryptionFlag:
    """Tests for encryption flag (placeholder for future implementation)."""

    def test_encryption_flag_in_updates(self):
        """Test that encryption flag is included in updates."""
        ctx = MockContext()
        store = LocalStore(ctx, encrypt=True)
        store.set("key", "value")
        updates = store._get_pending_updates()
        assert updates[0]["encrypt"] is True

    def test_no_encryption_by_default(self):
        """Test that encryption is disabled by default."""
        ctx = MockContext()
        store = LocalStore(ctx)
        store.set("key", "value")
        updates = store._get_pending_updates()
        assert updates[0]["encrypt"] is False



