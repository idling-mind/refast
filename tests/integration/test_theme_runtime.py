"""Integration tests for runtime theme updates via WebSocket."""

import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from refast import RefastApp
from refast.context import Context
from refast.theme import Theme, ThemeColors


class TestCtxSetTheme:
    """Tests for ctx.set_theme() and ctx.broadcast_theme()."""

    @pytest.mark.asyncio
    async def test_set_theme_sends_ws_message(self):
        """set_theme should push a theme_update message via WebSocket."""
        app = RefastApp()
        ws = AsyncMock()
        ctx = Context(websocket=ws, app=app)

        theme = Theme(
            light=ThemeColors(primary="100 50% 50%"),
            dark=ThemeColors(primary="200 60% 40%"),
            font_family="Roboto",
            radius="0.75rem",
        )

        await ctx.set_theme(theme)

        ws.send_json.assert_called_once()
        payload = ws.send_json.call_args[0][0]
        assert payload["type"] == "theme_update"
        assert payload["theme"]["light"] == {"--primary": "100 50% 50%"}
        assert payload["theme"]["dark"] == {"--primary": "200 60% 40%"}
        assert payload["theme"]["fontFamily"] == "Roboto"
        assert payload["theme"]["radius"] == "0.75rem"

    @pytest.mark.asyncio
    async def test_set_theme_updates_app_theme(self):
        """set_theme should also update app.theme for future page loads."""
        app = RefastApp()
        ws = AsyncMock()
        ctx = Context(websocket=ws, app=app)

        theme = Theme(light=ThemeColors(primary="1 2% 3%"))
        await ctx.set_theme(theme)

        assert app.theme is theme

    @pytest.mark.asyncio
    async def test_set_theme_no_websocket(self):
        """set_theme should not crash without a WebSocket."""
        app = RefastApp()
        ctx = Context(app=app)

        theme = Theme(light=ThemeColors(primary="1 2% 3%"))
        await ctx.set_theme(theme)  # should not raise

        assert app.theme is theme

    @pytest.mark.asyncio
    async def test_broadcast_theme_sends_to_all_clients(self):
        """broadcast_theme should send theme_update to all connected clients."""
        app = RefastApp()

        ws1 = AsyncMock()
        ws2 = AsyncMock()
        ctx1 = Context(websocket=ws1, app=app)
        ctx2 = Context(websocket=ws2, app=app)

        # Simulate active_contexts by patching
        with patch.object(
            type(app), "active_contexts", new_callable=lambda: property(lambda self: [ctx1, ctx2])
        ):
            theme = Theme(light=ThemeColors(primary="10 20% 30%"))
            count = await ctx1.broadcast_theme(theme)

        assert count == 2
        assert app.theme is theme

        # Both websockets should have received the message
        for ws in [ws1, ws2]:
            ws.send_json.assert_called_once()
            payload = ws.send_json.call_args[0][0]
            assert payload["type"] == "theme_update"
            assert payload["theme"]["light"] == {"--primary": "10 20% 30%"}

    @pytest.mark.asyncio
    async def test_broadcast_theme_no_app(self):
        """broadcast_theme should return 0 when no app is set."""
        ctx = Context()
        theme = Theme()
        count = await ctx.broadcast_theme(theme)
        assert count == 0

    @pytest.mark.asyncio
    async def test_broadcast_theme_handles_closed_connections(self):
        """broadcast_theme should skip failed connections gracefully."""
        app = RefastApp()

        ws_good = AsyncMock()
        ws_bad = AsyncMock()
        ws_bad.send_json.side_effect = Exception("Connection closed")

        ctx_good = Context(websocket=ws_good, app=app)
        ctx_bad = Context(websocket=ws_bad, app=app)

        with patch.object(
            type(app), "active_contexts", new_callable=lambda: property(lambda self: [ctx_bad, ctx_good])
        ):
            theme = Theme(light=ThemeColors(primary="5 5% 5%"))
            count = await ctx_good.broadcast_theme(theme)

        # Only the good one should count
        assert count == 1
        ws_good.send_json.assert_called_once()
