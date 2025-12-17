"""Session store implementations."""

from refast.session.stores.base import SessionStore
from refast.session.stores.memory import MemorySessionStore

__all__ = ["SessionStore", "MemorySessionStore"]

try:
    from refast.session.stores.redis import RedisSessionStore  # noqa: F401

    __all__.append("RedisSessionStore")
except ImportError:
    pass
