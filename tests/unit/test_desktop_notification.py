"""Tests for Context.show_desktop_notification() method."""

from unittest.mock import AsyncMock

import pytest

from refast.context import Callback, Context


class TestContextDesktopNotification:
    """Tests for Context.show_desktop_notification() method."""

    @pytest.mark.asyncio
    async def test_show_desktop_notification_sends_correct_message(self):
        """Test show_desktop_notification sends correct WebSocket message with parameters."""
        ws = AsyncMock()
        ctx = Context(websocket=ws)

        await ctx.show_desktop_notification(
            title="Test Title",
            body="Test Body",
            icon="/path/to/icon.png",
            tag="test-tag",
            silent=True,
            require_interaction=True,
        )

        ws.send_json.assert_called_once_with(
            {
                "type": "desktop_notification",
                "title": "Test Title",
                "body": "Test Body",
                "icon": "/path/to/icon.png",
                "tag": "test-tag",
                "silent": True,
                "require_interaction": True,
            }
        )

    @pytest.mark.asyncio
    async def test_show_desktop_notification_serializes_callbacks(self):
        """Test that callbacks are serialized correctly."""
        ws = AsyncMock()
        ctx = Context(websocket=ws)

        def click_handler():
            pass

        def close_handler():
            pass

        def granted_handler():
            pass

        def denied_handler():
            pass

        cb_click = ctx.callback(click_handler)
        cb_close = ctx.callback(close_handler)
        cb_granted = ctx.callback(granted_handler)
        cb_denied = ctx.callback(denied_handler)

        await ctx.show_desktop_notification(
            title="Title",
            on_click=cb_click,
            on_close=cb_close,
            on_permission_granted=cb_granted,
            on_permission_denied=cb_denied,
        )

        call_args = ws.send_json.call_args[0][0]
        assert call_args["type"] == "desktop_notification"
        assert call_args["title"] == "Title"
        assert call_args["on_click"] == cb_click.serialize()
        assert call_args["on_close"] == cb_close.serialize()
        assert call_args["on_permission_granted"] == cb_granted.serialize()
        assert call_args["on_permission_denied"] == cb_denied.serialize()

    @pytest.mark.asyncio
    async def test_show_desktop_notification_without_websocket(self):
        """Test show_desktop_notification does nothing and does not raise without websocket."""
        ctx = Context()
        # Should not raise
        await ctx.show_desktop_notification(
            title="Title",
            body="Body",
        )
