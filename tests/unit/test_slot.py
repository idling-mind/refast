"""Tests for Slot component."""

from refast.components.base import Text
from refast.components.slot import Slot


class TestSlot:
    """Tests for Slot component."""

    def test_slot_renders(self):
        """Test Slot renders correctly."""
        slot = Slot(id="my-slot")
        rendered = slot.render()
        assert rendered["type"] == "Slot"
        assert rendered["id"] == "my-slot"

    def test_slot_with_children(self):
        """Test Slot with children."""
        slot = Slot(id="my-slot", children=[Text("Content")])
        rendered = slot.render()
        assert len(rendered["children"]) == 1
        assert rendered["children"][0]["type"] == "Text"

    def test_slot_with_fallback(self):
        """Test Slot with fallback and no children."""
        slot = Slot(id="my-slot", fallback=Text("Loading..."))
        rendered = slot.render()
        assert len(rendered["children"]) == 1
        assert rendered["children"][0]["children"] == ["Loading..."]

    def test_slot_children_override_fallback(self):
        """Test children take precedence over fallback."""
        slot = Slot(
            id="my-slot",
            children=[Text("Actual Content")],
            fallback=Text("Fallback Content"),
        )
        rendered = slot.render()
        assert len(rendered["children"]) == 1
        assert rendered["children"][0]["children"] == ["Actual Content"]

    def test_slot_with_class_name(self):
        """Test Slot with class_name."""
        slot = Slot(id="my-slot", class_name="loading-area")
        rendered = slot.render()
        assert rendered["props"]["className"] == "loading-area"

    def test_slot_empty(self):
        """Test Slot with no children or fallback."""
        slot = Slot(id="empty-slot")
        rendered = slot.render()
        assert rendered["children"] == []
