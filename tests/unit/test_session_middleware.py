"""Tests for SessionMiddleware."""

import pytest
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient

from refast.session.middleware import SessionMiddleware, get_session
from refast.session.stores.memory import MemorySessionStore


class TestSessionMiddleware:
    """Tests for SessionMiddleware class."""

    @pytest.fixture
    def store(self):
        """Create a memory store fixture."""
        return MemorySessionStore()

    @pytest.fixture
    def app_with_session(self, store):
        """Create a FastAPI app with session middleware."""
        app = FastAPI()
        app.add_middleware(SessionMiddleware, store=store)

        @app.get("/set/{key}/{value}")
        async def set_value(request: Request, key: str, value: str):
            request.state.session.set(key, value)
            return {"set": key}

        @app.get("/get/{key}")
        async def get_value(request: Request, key: str):
            return {"value": request.state.session.get(key)}

        @app.get("/id")
        async def get_session_id(request: Request):
            return {"session_id": request.state.session.id}

        return app

    def test_session_available(self, app_with_session):
        """Test session is available on request."""
        client = TestClient(app_with_session)
        response = client.get("/id")
        assert response.status_code == 200
        assert "session_id" in response.json()

    def test_session_cookie_set(self, app_with_session):
        """Test session cookie is set."""
        client = TestClient(app_with_session)
        response = client.get("/get/anything")
        assert "refast_session" in response.cookies

    def test_session_persists(self, app_with_session):
        """Test session data persists across requests."""
        client = TestClient(app_with_session)

        # Set a value
        response = client.get("/set/name/Alice")
        assert response.status_code == 200

        # Get the value (same session via cookies)
        response = client.get("/get/name")
        assert response.json()["value"] == "Alice"

    def test_session_id_persists(self, app_with_session):
        """Test session ID persists across requests when data is set."""
        client = TestClient(app_with_session)

        # Set a value to trigger save
        response1 = client.get("/set/test/value")
        assert response1.status_code == 200

        # Get session ID
        response2 = client.get("/id")
        session_id_1 = response2.json()["session_id"]

        # Get session ID again
        response3 = client.get("/id")
        session_id_2 = response3.json()["session_id"]

        assert session_id_1 == session_id_2

    def test_new_session_without_cookie(self, app_with_session):
        """Test new session is created without cookie."""
        client = TestClient(app_with_session, cookies={})
        response = client.get("/id")
        assert response.status_code == 200
        assert response.json()["session_id"] is not None


class TestGetSessionDependency:
    """Tests for get_session dependency."""

    @pytest.fixture
    def app_with_dependency(self):
        """Create app using get_session dependency."""
        from fastapi import Depends

        from refast.session.session import Session

        app = FastAPI()
        store = MemorySessionStore()
        app.add_middleware(SessionMiddleware, store=store)

        @app.get("/session-id")
        async def get_id(session: Session = Depends(get_session)):
            return {"id": session.id}

        @app.get("/set/{key}/{value}")
        async def set_val(key: str, value: str, session: Session = Depends(get_session)):
            session.set(key, value)
            return {"set": key}

        @app.get("/get/{key}")
        async def get_val(key: str, session: Session = Depends(get_session)):
            return {"value": session.get(key)}

        return app

    def test_dependency_works(self, app_with_dependency):
        """Test get_session dependency works."""
        client = TestClient(app_with_dependency)
        response = client.get("/session-id")
        assert response.status_code == 200
        assert "id" in response.json()

    def test_dependency_set_get(self, app_with_dependency):
        """Test set and get via dependency."""
        client = TestClient(app_with_dependency)

        response = client.get("/set/foo/bar")
        assert response.status_code == 200

        response = client.get("/get/foo")
        assert response.json()["value"] == "bar"


class TestSessionMiddlewareOptions:
    """Tests for middleware configuration options."""

    def test_custom_cookie_name(self):
        """Test custom cookie name."""
        app = FastAPI()
        store = MemorySessionStore()
        app.add_middleware(SessionMiddleware, store=store, cookie_name="my_session")

        @app.get("/")
        async def home(request: Request):
            return {"ok": True}

        client = TestClient(app)
        response = client.get("/")
        assert "my_session" in response.cookies

    def test_default_store(self):
        """Test default memory store is created."""
        app = FastAPI()
        # No store provided - should use MemorySessionStore
        app.add_middleware(SessionMiddleware)

        @app.get("/")
        async def home(request: Request):
            request.state.session.set("test", "value")
            return {"ok": True}

        client = TestClient(app)
        response = client.get("/")
        assert response.status_code == 200
