"""Tests for WebSocket message validation using Pydantic."""

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import ValidationError

from refast import RefastApp
from refast.components import Button
from refast.models.messages import (
    CallbackMessage,
    EventMessage,
    NavigateMessage,
    StoreInitMessage,
    StoreSyncMessage,
    client_message_adapter,
)


def test_valid_callback_message():
    """Test parsing a valid callback message."""
    data = {
        "type": "callback",
        "callbackId": "test-id-123",
        "data": {"foo": "bar"},
        "eventData": {"value": "hello"},
    }
    msg = client_message_adapter.validate_python(data)
    assert isinstance(msg, CallbackMessage)
    assert msg.type == "callback"
    assert msg.callback_id == "test-id-123"
    assert msg.data == {"foo": "bar"}
    assert msg.event_data == {"value": "hello"}


def test_valid_store_init_message():
    """Test parsing a valid store_init message."""
    data = {
        "type": "store_init",
        "data": {"session_var": "val"},
        "path": "/dashboard",
    }
    msg = client_message_adapter.validate_python(data)
    assert isinstance(msg, StoreInitMessage)
    assert msg.type == "store_init"
    assert msg.data == {"session_var": "val"}
    assert msg.path == "/dashboard"


def test_valid_navigate_message():
    """Test parsing a valid navigate message."""
    data = {
        "type": "navigate",
        "path": "/profile",
    }
    msg = client_message_adapter.validate_python(data)
    assert isinstance(msg, NavigateMessage)
    assert msg.type == "navigate"
    assert msg.path == "/profile"


def test_valid_event_message():
    """Test parsing a valid event message."""
    data = {
        "type": "event",
        "eventType": "custom_click",
        "data": {"x": 10},
    }
    msg = client_message_adapter.validate_python(data)
    assert isinstance(msg, EventMessage)
    assert msg.type == "event"
    assert msg.event_type == "custom_click"
    assert msg.data == {"x": 10}


def test_valid_store_sync_message():
    """Test parsing a valid store_sync message."""
    data = {
        "type": "store_sync",
        "data": {"a": 1},
    }
    msg = client_message_adapter.validate_python(data)
    assert isinstance(msg, StoreSyncMessage)
    assert msg.type == "store_sync"
    assert msg.data == {"a": 1}


def test_invalid_message_missing_discriminator():
    """Test that messages without a type fail validation."""
    data = {
        "callbackId": "123",
    }
    with pytest.raises(ValidationError):
        client_message_adapter.validate_python(data)


def test_invalid_message_wrong_discriminator():
    """Test that messages with an invalid type fail validation."""
    data = {
        "type": "invalid_type",
    }
    with pytest.raises(ValidationError):
        client_message_adapter.validate_python(data)


def test_invalid_callback_message_missing_id():
    """Test that callback message missing callbackId fails validation."""
    data = {
        "type": "callback",
    }
    with pytest.raises(ValidationError):
        client_message_adapter.validate_python(data)


def test_websocket_validation_error_response():
    """Test that sending invalid message over WS returns validation_error."""
    ui = RefastApp()

    @ui.page("/")
    def home(ctx):
        return Button("Click")

    app = FastAPI()
    app.include_router(ui.router)
    client = TestClient(app)

    with client.websocket_connect("/ws") as ws:
        # Send invalid message (missing callbackId)
        ws.send_json({
            "type": "callback",
            "data": {},
        })
        # Expect a validation_error response
        resp = ws.receive_json()
        assert resp["type"] == "validation_error"
        assert "details" in resp
        assert len(resp["details"]) > 0
        # Check that missing callback_id is reported
        err = resp["details"][0]
        # Pydantic 2 paths/loc might be 'callbackId' or 'callback_id' depending on alias generators,
        # but loc will contain the field name.
        assert "callbackId" in err["loc"] or "callback_id" in err["loc"]
