"""Tests for Context.refresh functionality."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from refast.components.base import Component
from refast.context import Context


class MockComponent(Component):
    """Component for testing."""

    component_type = "MockComponent"

    def render(self) -> dict:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {},
            "children": self._render_children(),
        }


@pytest.mark.asyncio
class TestContextRefresh:
    """Tests for Context.refresh() method."""

    async def test_full_refresh(self):
        """Test full page refresh behavior."""
        mock_ws = AsyncMock()
        mock_app = MagicMock()

        # Setup page function
        component = MockComponent(id="page-root")
        mock_page_func = MagicMock(return_value=component)
        mock_app._pages = {"/": mock_page_func}

        ctx = Context(websocket=mock_ws, app=mock_app)

        await ctx.refresh()

        # Verify page accessed and rendered
        mock_page_func.assert_called_with(ctx)
        mock_ws.send_json.assert_called_with({"type": "refresh", "component": component.render()})

    async def test_partial_refresh_found(self):
        """Test partial refresh when target component is found."""
        mock_ws = AsyncMock()
        mock_app = MagicMock()

        # Setup page with nested structure
        target_id = "target-comp"
        target_comp = MockComponent(id=target_id)
        parent_comp = MockComponent(id="parent")
        parent_comp.add_child(target_comp)

        mock_page_func = MagicMock(return_value=parent_comp)
        mock_app._pages = {"/": mock_page_func}

        ctx = Context(websocket=mock_ws, app=mock_app)

        await ctx.refresh(target_id=target_id)

        # Verify only target component sent as update/replace
        mock_page_func.assert_called_with(ctx)
        mock_ws.send_json.assert_called_with(
            {
                "type": "update",
                "targetId": target_id,
                "operation": "replace",
                "component": target_comp.render(),
            }
        )

    async def test_partial_refresh_not_found(self):
        """Test partial refresh when target component is NOT found."""
        mock_ws = AsyncMock()
        mock_app = MagicMock()

        # Setup page without target component
        page_comp = MockComponent(id="page-root")
        mock_page_func = MagicMock(return_value=page_comp)
        mock_app._pages = {"/": mock_page_func}

        ctx = Context(websocket=mock_ws, app=mock_app)

        await ctx.refresh(target_id="missing-id")

        # Verify page rendered but no update sent
        mock_page_func.assert_called_with(ctx)
        mock_ws.send_json.assert_not_called()

    async def test_refresh_with_path(self):
        """Test refresh with specific path."""
        mock_ws = AsyncMock()
        mock_app = MagicMock()

        path = "/dashboard"
        component = MockComponent(id="dashboard-root")
        mock_page_func = MagicMock(return_value=component)
        mock_app._pages = {path: mock_page_func}

        ctx = Context(websocket=mock_ws, app=mock_app)

        await ctx.refresh(path=path)

        # Verify correct page func called
        # Note: We can't assert calls on _pages.get because it's a real dict method
        mock_page_func.assert_called_with(ctx)
