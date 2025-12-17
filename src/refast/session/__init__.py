"""Session management system."""

from refast.session.middleware import SessionMiddleware, get_session
from refast.session.session import Session, SessionData
from refast.session.stores.base import SessionStore
from refast.session.stores.memory import MemorySessionStore

__all__ = [
    "Session",
    "SessionData",
    "SessionStore",
    "MemorySessionStore",
    "SessionMiddleware",
    "get_session",
]

# Optional Redis import
try:
    from refast.session.stores.redis import RedisSessionStore  # noqa: F401

    __all__.append("RedisSessionStore")
except ImportError:
    pass
