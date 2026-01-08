"""Tests for typography components."""

from refast.components.shadcn.typography import Code, Heading, Link, Paragraph


class MockCallback:
    """Mock callback for testing."""

    def serialize(self):
        return {"callbackId": "cb-123"}


class TestHeading:
    """Tests for Heading component."""

    def test_heading_renders(self):
        """Test Heading renders correctly."""
        h = Heading("Title")
        rendered = h.render()
        assert rendered["type"] == "Heading"
        assert rendered["children"] == ["Title"]
        assert rendered["props"]["level"] == 1

    def test_heading_levels(self):
        """Test Heading with different levels."""
        for level in [1, 2, 3, 4, 5, 6]:
            h = Heading("Test", level=level)
            rendered = h.render()
            assert rendered["props"]["level"] == level

    def test_heading_with_class(self):
        """Test Heading with class_name."""
        h = Heading("Title", class_name="text-blue-500")
        rendered = h.render()
        assert rendered["props"]["className"] == "text-blue-500"


class TestParagraph:
    """Tests for Paragraph component."""

    def test_paragraph_renders(self):
        """Test Paragraph renders correctly."""
        p = Paragraph("Some text content.")
        rendered = p.render()
        assert rendered["type"] == "Paragraph"
        assert rendered["children"] == ["Some text content."]

    def test_paragraph_with_class(self):
        """Test Paragraph with class_name."""
        p = Paragraph("Text", class_name="text-gray-600")
        rendered = p.render()
        assert rendered["props"]["className"] == "text-gray-600"


class TestCode:
    """Tests for Code component."""

    def test_code_renders(self):
        """Test Code renders correctly."""
        code = Code("const x = 1;")
        rendered = code.render()
        assert rendered["type"] == "Code"
        assert rendered["children"] == ["const x = 1;"]

    def test_code_with_language(self):
        """Test Code with language prop."""
        code = Code("def foo():\n    pass", language="python")
        rendered = code.render()
        assert rendered["props"]["language"] == "python"

    def test_code_inline(self):
        """Test Code inline mode."""
        code = Code("variable", inline=True)
        rendered = code.render()
        assert rendered["props"]["inline"] is True


class TestLink:
    """Tests for Link component."""

    def test_link_renders(self):
        """Test Link renders correctly."""
        link = Link("Click here", href="/page")
        rendered = link.render()
        assert rendered["type"] == "Link"
        assert rendered["children"] == ["Click here"]
        assert rendered["props"]["href"] == "/page"

    def test_link_target(self):
        """Test Link target prop."""
        link = Link("External", href="https://example.com", target="_blank")
        rendered = link.render()
        assert rendered["props"]["target"] == "_blank"

    def test_link_with_callback(self):
        """Test Link with on_click callback."""
        cb = MockCallback()
        link = Link("Click", href="#", on_click=cb)
        rendered = link.render()
        assert rendered["props"]["onClick"] == {"callbackId": "cb-123"}
