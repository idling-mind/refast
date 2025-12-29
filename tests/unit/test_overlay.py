"""Tests for overlay components (Stage 9)."""


from refast.components.shadcn.button import Button
from refast.components.shadcn.overlay import (
    AlertDialog,
    AlertDialogAction,
    AlertDialogCancel,
    AlertDialogContent,
    AlertDialogDescription,
    AlertDialogFooter,
    AlertDialogHeader,
    AlertDialogTitle,
    AlertDialogTrigger,
    Drawer,
    HoverCard,
    Popover,
    Sheet,
    SheetContent,
)


class MockCallback:
    """Mock callback for testing."""

    def serialize(self):
        return {"callbackId": "cb-123"}


class TestAlertDialog:
    """Tests for AlertDialog component."""

    def test_alert_dialog_renders(self):
        """Test AlertDialog renders correctly."""
        dialog = AlertDialog()
        rendered = dialog.render()
        assert rendered["type"] == "AlertDialog"

    def test_alert_dialog_with_children(self):
        """Test AlertDialog with composition-based children."""
        dialog = AlertDialog(
            children=[
                AlertDialogTrigger(children=Button(label="Open")),
                AlertDialogContent(
                    children=[
                        AlertDialogHeader(
                            children=[
                                AlertDialogTitle(title="Confirm Action"),
                                AlertDialogDescription(description="Are you sure?"),
                            ]
                        ),
                        AlertDialogFooter(
                            children=[
                                AlertDialogCancel(label="Cancel"),
                                AlertDialogAction(label="Continue"),
                            ]
                        ),
                    ]
                ),
            ]
        )
        rendered = dialog.render()
        assert rendered["type"] == "AlertDialog"
        assert len(rendered["children"]) == 2

    def test_alert_dialog_default_open(self):
        """Test AlertDialog default open state."""
        dialog = AlertDialog(default_open=True)
        rendered = dialog.render()
        assert rendered["props"]["defaultOpen"] is True

    def test_alert_dialog_open_state(self):
        """Test AlertDialog open state."""
        dialog = AlertDialog(open=True)
        rendered = dialog.render()
        assert rendered["props"]["open"] is True

    def test_alert_dialog_with_callback(self):
        """Test AlertDialog with onOpenChange callback."""
        cb = MockCallback()
        dialog = AlertDialog(on_open_change=cb)
        rendered = dialog.render()
        assert rendered["props"]["onOpenChange"] == {"callbackId": "cb-123"}


class TestSheet:
    """Tests for Sheet component."""

    def test_sheet_renders(self):
        """Test Sheet renders correctly."""
        sheet = Sheet()
        rendered = sheet.render()
        assert rendered["type"] == "Sheet"

    def test_sheet_content_side_left(self):
        """Test SheetContent from left side."""
        content = SheetContent(side="left")
        rendered = content.render()
        assert rendered["props"]["side"] == "left"

    def test_sheet_content_side_right(self):
        """Test SheetContent from right side (default)."""
        content = SheetContent()
        rendered = content.render()
        assert rendered["props"]["side"] == "right"

    def test_sheet_content_side_top(self):
        """Test SheetContent from top."""
        content = SheetContent(side="top")
        rendered = content.render()
        assert rendered["props"]["side"] == "top"

    def test_sheet_content_side_bottom(self):
        """Test SheetContent from bottom."""
        content = SheetContent(side="bottom")
        rendered = content.render()
        assert rendered["props"]["side"] == "bottom"

    def test_sheet_default_open(self):
        """Test Sheet default open state."""
        sheet = Sheet(default_open=True)
        rendered = sheet.render()
        assert rendered["props"]["defaultOpen"] is True

    def test_sheet_open_state(self):
        """Test Sheet open state."""
        sheet = Sheet(open=True)
        rendered = sheet.render()
        assert rendered["props"]["open"] is True

    def test_sheet_with_callback(self):
        """Test Sheet with onOpenChange callback."""
        cb = MockCallback()
        sheet = Sheet(on_open_change=cb)
        rendered = sheet.render()
        assert rendered["props"]["onOpenChange"] == {"callbackId": "cb-123"}


class TestDrawer:
    """Tests for Drawer component."""

    def test_drawer_renders(self):
        """Test Drawer renders correctly."""
        drawer = Drawer()
        rendered = drawer.render()
        assert rendered["type"] == "Drawer"

    def test_drawer_should_scale_background(self):
        """Test Drawer should scale background option."""
        drawer = Drawer(should_scale_background=False)
        rendered = drawer.render()
        assert rendered["props"]["shouldScaleBackground"] is False

    def test_drawer_open_state(self):
        """Test Drawer open state."""
        drawer = Drawer(open=True)
        rendered = drawer.render()
        assert rendered["props"]["open"] is True

    def test_drawer_with_callback(self):
        """Test Drawer with onOpenChange callback."""
        cb = MockCallback()
        drawer = Drawer(on_open_change=cb)
        rendered = drawer.render()
        assert rendered["props"]["onOpenChange"] == {"callbackId": "cb-123"}


class TestHoverCard:
    """Tests for HoverCard component."""

    def test_hover_card_renders(self):
        """Test HoverCard renders correctly."""
        card = HoverCard()
        rendered = card.render()
        assert rendered["type"] == "HoverCard"

    def test_hover_card_delays(self):
        """Test HoverCard with custom delays."""
        card = HoverCard(open_delay=500, close_delay=200)
        rendered = card.render()
        assert rendered["props"]["openDelay"] == 500
        assert rendered["props"]["closeDelay"] == 200

    def test_hover_card_default_delays(self):
        """Test HoverCard default delay values."""
        card = HoverCard()
        rendered = card.render()
        assert rendered["props"]["openDelay"] == 700
        assert rendered["props"]["closeDelay"] == 300

    def test_hover_card_open_state(self):
        """Test HoverCard open state."""
        card = HoverCard(open=True)
        rendered = card.render()
        assert rendered["props"]["open"] is True


class TestPopover:
    """Tests for Popover component."""

    def test_popover_renders(self):
        """Test Popover renders correctly."""
        popover = Popover()
        rendered = popover.render()
        assert rendered["type"] == "Popover"

    def test_popover_open_state(self):
        """Test Popover open state."""
        popover = Popover(open=True)
        rendered = popover.render()
        assert rendered["props"]["open"] is True

    def test_popover_default_open(self):
        """Test Popover default open state."""
        popover = Popover(default_open=True)
        rendered = popover.render()
        assert rendered["props"]["defaultOpen"] is True

    def test_popover_with_callback(self):
        """Test Popover with onOpenChange callback."""
        cb = MockCallback()
        popover = Popover(on_open_change=cb)
        rendered = popover.render()
        assert rendered["props"]["onOpenChange"] == {"callbackId": "cb-123"}
