"""Tests for Session and SessionData classes."""

import pytest
from datetime import timedelta, timezone, datetime
from refast.session.session import Session, SessionData


def _now_utc() -> datetime:
    """Get current UTC time."""
    return datetime.now(timezone.utc)


class TestSessionData:
    """Tests for SessionData class."""

    def test_session_data_has_id(self):
        """Test session data has unique ID."""
        data = SessionData()
        assert data.id is not None
        assert len(data.id) > 0

    def test_session_data_unique_ids(self):
        """Test session data has unique IDs."""
        data1 = SessionData()
        data2 = SessionData()
        assert data1.id != data2.id

    def test_session_data_defaults(self):
        """Test session data default values."""
        data = SessionData()
        assert data.data == {}
        assert data.expires_at is None
        assert isinstance(data.created_at, datetime)
        assert isinstance(data.updated_at, datetime)

    def test_session_data_not_expired_by_default(self):
        """Test session data not expired by default."""
        data = SessionData()
        assert not data.is_expired()

    def test_session_data_not_expired_future(self):
        """Test session data with future expiry is not expired."""
        data = SessionData(expires_at=_now_utc() + timedelta(hours=1))
        assert not data.is_expired()

    def test_session_data_expired(self):
        """Test session data with past expiry is expired."""
        data = SessionData(expires_at=_now_utc() - timedelta(hours=1))
        assert data.is_expired()

    def test_session_data_to_dict(self):
        """Test converting session data to dictionary."""
        data = SessionData(data={"key": "value"})
        d = data.to_dict()
        assert d["data"]["key"] == "value"
        assert "id" in d
        assert "created_at" in d
        assert "updated_at" in d

    def test_session_data_from_dict(self):
        """Test creating session data from dictionary."""
        now = _now_utc()
        d = {
            "id": "test-id",
            "data": {"foo": "bar"},
            "created_at": now.isoformat(),
            "updated_at": now.isoformat(),
            "expires_at": None,
        }
        data = SessionData.from_dict(d)
        assert data.id == "test-id"
        assert data.data["foo"] == "bar"

    def test_session_data_roundtrip(self):
        """Test session data serialization roundtrip."""
        original = SessionData(
            data={"user_id": 123, "name": "Alice"},
            expires_at=_now_utc() + timedelta(hours=1),
        )
        d = original.to_dict()
        restored = SessionData.from_dict(d)
        assert restored.id == original.id
        assert restored.data == original.data


class TestSession:
    """Tests for Session class."""

    def test_session_has_id(self):
        """Test session has ID."""
        session = Session()
        assert session.id is not None

    def test_session_id_alias(self):
        """Test session_id is alias for id."""
        session = Session()
        assert session.id == session.session_id

    def test_session_get_set(self):
        """Test session get and set."""
        session = Session()
        session.set("key", "value")
        assert session.get("key") == "value"

    def test_session_get_default(self):
        """Test session get with default."""
        session = Session()
        assert session.get("missing", "default") == "default"

    def test_session_get_none_default(self):
        """Test session get returns None by default."""
        session = Session()
        assert session.get("missing") is None

    def test_session_dict_access(self):
        """Test session dict-like access."""
        session = Session()
        session["key"] = "value"
        assert session["key"] == "value"

    def test_session_dict_delete(self):
        """Test session dict-like deletion."""
        session = Session()
        session["key"] = "value"
        del session["key"]
        assert "key" not in session

    def test_session_contains(self):
        """Test session contains check."""
        session = Session()
        session.set("key", "value")
        assert "key" in session
        assert "missing" not in session

    def test_session_delete(self):
        """Test session delete."""
        session = Session()
        session.set("key", "value")
        session.delete("key")
        assert "key" not in session

    def test_session_delete_nonexistent(self):
        """Test deleting nonexistent key is safe."""
        session = Session()
        session.delete("nonexistent")  # Should not raise

    def test_session_clear(self):
        """Test session clear."""
        session = Session()
        session.set("a", 1)
        session.set("b", 2)
        session.clear()
        assert len(session.keys()) == 0

    def test_session_keys(self):
        """Test getting session keys."""
        session = Session()
        session.set("a", 1)
        session.set("b", 2)
        assert sorted(session.keys()) == ["a", "b"]

    def test_session_values(self):
        """Test getting session values."""
        session = Session()
        session.set("a", 1)
        session.set("b", 2)
        assert sorted(session.values()) == [1, 2]

    def test_session_items(self):
        """Test getting session items."""
        session = Session()
        session.set("a", 1)
        assert ("a", 1) in session.items()

    def test_session_modified_flag_initial(self):
        """Test session is not modified initially."""
        session = Session()
        assert not session.is_modified

    def test_session_modified_after_set(self):
        """Test session is modified after set."""
        session = Session()
        session.set("key", "value")
        assert session.is_modified

    def test_session_modified_after_dict_set(self):
        """Test session is modified after dict assignment."""
        session = Session()
        session["key"] = "value"
        assert session.is_modified

    def test_session_modified_after_delete(self):
        """Test session is modified after delete."""
        session = Session()
        session.set("key", "value")
        session._modified = False  # Reset
        session.delete("key")
        assert session.is_modified

    def test_session_modified_after_clear(self):
        """Test session is modified after clear."""
        session = Session()
        session.set("key", "value")
        session._modified = False  # Reset
        session.clear()
        assert session.is_modified

    def test_session_set_expiry(self):
        """Test setting session expiry."""
        session = Session()
        session.set_expiry(3600)
        assert not session.is_expired
        assert session._data.expires_at is not None

    def test_session_to_dict(self):
        """Test session to_dict."""
        session = Session()
        session.set("key", "value")
        d = session.to_dict()
        assert d["data"]["key"] == "value"

    def test_session_repr(self):
        """Test session string representation."""
        session = Session()
        session.set("key", "value")
        r = repr(session)
        assert "Session" in r
        assert "key" in r

    def test_session_created_at(self):
        """Test session creation time."""
        session = Session()
        assert isinstance(session.created_at, datetime)

    def test_session_updated_at(self):
        """Test session update time."""
        session = Session()
        assert isinstance(session.updated_at, datetime)
