"""Tests for button and card components."""


from refast.components.base import Text
from refast.components.shadcn.button import Button, IconButton
from refast.components.shadcn.card import Card, CardContent, CardFooter, CardHeader


class MockCallback:
    """Mock callback for testing."""

    def serialize(self):
        return {"callbackId": "cb-123"}


class TestButton:
    """Tests for Button component."""

    def test_button_renders(self):
        """Test Button renders correctly."""
        btn = Button("Click Me")
        rendered = btn.render()
        assert rendered["type"] == "Button"
        assert rendered["children"] == ["Click Me"]

    def test_button_variant(self):
        """Test Button variant prop."""
        btn = Button("Test", variant="primary")
        rendered = btn.render()
        assert rendered["props"]["variant"] == "primary"

    def test_button_size(self):
        """Test Button size prop."""
        btn = Button("Test", size="lg")
        rendered = btn.render()
        assert rendered["props"]["size"] == "lg"

    def test_button_disabled(self):
        """Test Button disabled prop."""
        btn = Button("Test", disabled=True)
        rendered = btn.render()
        assert rendered["props"]["disabled"] is True

    def test_button_loading(self):
        """Test Button loading state disables button."""
        btn = Button("Test", loading=True)
        rendered = btn.render()
        assert rendered["props"]["loading"] is True
        assert rendered["props"]["disabled"] is True

    def test_button_type(self):
        """Test Button type prop."""
        btn = Button("Submit", type="submit")
        rendered = btn.render()
        assert rendered["props"]["type"] == "submit"

    def test_button_with_callback(self):
        """Test Button with on_click callback."""
        cb = MockCallback()
        btn = Button("Test", on_click=cb)
        rendered = btn.render()
        assert rendered["props"]["onClick"] == {"callbackId": "cb-123"}


class TestIconButton:
    """Tests for IconButton component."""

    def test_icon_button_renders(self):
        """Test IconButton renders correctly."""
        btn = IconButton(icon="trash")
        rendered = btn.render()
        assert rendered["type"] == "IconButton"
        assert rendered["props"]["icon"] == "trash"

    def test_icon_button_variant(self):
        """Test IconButton variant prop."""
        btn = IconButton(icon="edit", variant="outline")
        rendered = btn.render()
        assert rendered["props"]["variant"] == "outline"

    def test_icon_button_aria_label(self):
        """Test IconButton aria_label prop."""
        btn = IconButton(icon="close", aria_label="Close dialog")
        rendered = btn.render()
        assert rendered["props"]["ariaLabel"] == "Close dialog"

    def test_icon_button_with_callback(self):
        """Test IconButton with on_click callback."""
        cb = MockCallback()
        btn = IconButton(icon="save", on_click=cb)
        rendered = btn.render()
        assert rendered["props"]["onClick"] == {"callbackId": "cb-123"}


class TestCard:
    """Tests for Card component."""

    def test_card_renders(self):
        """Test Card renders correctly."""
        card = Card(title="My Card")
        rendered = card.render()
        assert rendered["type"] == "Card"
        assert rendered["props"]["title"] == "My Card"

    def test_card_with_description(self):
        """Test Card with description."""
        card = Card(title="Title", description="Description text")
        rendered = card.render()
        assert rendered["props"]["description"] == "Description text"

    def test_card_with_children(self):
        """Test Card with children."""
        card = Card(children=[Text("Content")])
        rendered = card.render()
        assert len(rendered["children"]) == 1

    def test_card_with_callback(self):
        """Test Card with on_click callback."""
        cb = MockCallback()
        card = Card(on_click=cb)
        rendered = card.render()
        assert rendered["props"]["onClick"] == {"callbackId": "cb-123"}


class TestCardHeader:
    """Tests for CardHeader component."""

    def test_card_header_renders(self):
        """Test CardHeader renders correctly."""
        header = CardHeader(title="Header Title", description="Subtitle")
        rendered = header.render()
        assert rendered["type"] == "CardHeader"
        assert rendered["props"]["title"] == "Header Title"
        assert rendered["props"]["description"] == "Subtitle"


class TestCardContent:
    """Tests for CardContent component."""

    def test_card_content_renders(self):
        """Test CardContent renders correctly."""
        content = CardContent(children=[Text("Body text")])
        rendered = content.render()
        assert rendered["type"] == "CardContent"
        assert len(rendered["children"]) == 1


class TestCardFooter:
    """Tests for CardFooter component."""

    def test_card_footer_renders(self):
        """Test CardFooter renders correctly."""
        footer = CardFooter(children=[Button("Action")])
        rendered = footer.render()
        assert rendered["type"] == "CardFooter"
        assert len(rendered["children"]) == 1
