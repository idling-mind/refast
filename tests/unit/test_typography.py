"""Tests for typography components."""

from refast.components.base import Container, Text
from refast.components.shadcn.typography import BlockQuote, Code, Heading, Link, Markdown, Paragraph


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
        assert rendered["props"]["class_name"] == "text-blue-500"


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
        assert rendered["props"]["class_name"] == "text-gray-600"


class TestCode:
    """Tests for Code component."""

    def test_code_renders(self):
        """Test Code renders correctly."""
        code = Code("const x = 1;")
        rendered = code.render()
        assert rendered["type"] == "Code"
        assert rendered["props"]["code"] == "const x = 1;"
        # Default inline should be True
        assert rendered["props"]["inline"] is True

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

    def test_code_block_mode(self):
        """Test Code block mode (non-inline)."""
        code = Code("def foo():\n    pass", language="python", inline=False)
        rendered = code.render()
        assert rendered["props"]["inline"] is False

    def test_code_with_class_name(self):
        """Test Code with class_name prop renders as className."""
        code = Code("code", class_name="my-class")
        rendered = code.render()
        assert rendered["props"]["class_name"] == "my-class"


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
        assert rendered["props"]["on_click"] == {"callbackId": "cb-123"}


class TestMarkdown:
    """Tests for Markdown component."""

    def test_markdown_renders(self):
        """Test Markdown renders correctly."""
        md = Markdown("# Hello World")
        rendered = md.render()
        assert rendered["type"] == "Markdown"
        assert rendered["props"]["content"] == "# Hello World"

    def test_markdown_with_content(self):
        """Test Markdown with full content."""
        content = """
# Title

This is **bold** and *italic* text.

- Item 1
- Item 2
"""
        md = Markdown(content)
        rendered = md.render()
        assert rendered["props"]["content"] == content

    def test_markdown_enable_latex_default(self):
        """Test Markdown enable_latex defaults to False."""
        md = Markdown("$E = mc^2$")
        rendered = md.render()
        assert rendered["props"]["enable_latex"] is False

    def test_markdown_enable_latex_enabled(self):
        """Test Markdown with LaTeX enabled."""
        md = Markdown("$E = mc^2$", enable_latex=True)
        rendered = md.render()
        assert rendered["props"]["enable_latex"] is True

    def test_markdown_allow_html_default(self):
        """Test Markdown allow_html defaults to False for security."""
        md = Markdown("<script>alert('xss')</script>")
        rendered = md.render()
        assert rendered["props"]["allow_html"] is False

    def test_markdown_allow_html_enabled(self):
        """Test Markdown with HTML enabled."""
        md = Markdown("<div>Custom HTML</div>", allow_html=True)
        rendered = md.render()
        assert rendered["props"]["allow_html"] is True

    def test_markdown_with_class_name(self):
        """Test Markdown with custom class_name."""
        md = Markdown("Content", class_name="prose-lg")
        rendered = md.render()
        assert rendered["props"]["class_name"] == "prose-lg"

    def test_markdown_with_latex_content(self):
        """Test Markdown with inline and display LaTeX."""
        content = """
Inline math: $E = mc^2$

Display math:
$$
\\int_0^\\infty e^{-x^2} dx = \\frac{\\sqrt{\\pi}}{2}
$$
"""
        md = Markdown(content, enable_latex=True)
        rendered = md.render()
        assert rendered["props"]["content"] == content
        assert rendered["props"]["enable_latex"] is True

    def test_markdown_children_empty(self):
        """Test Markdown has no children (content is in props)."""
        md = Markdown("Content")
        rendered = md.render()
        assert rendered["children"] == []


class TestBlockQuote:
    """Tests for BlockQuote component."""

    def test_blockquote_type(self):
        """Test BlockQuote renders with correct type."""
        bq = BlockQuote("Some quote")
        rendered = bq.render()
        assert rendered["type"] == "BlockQuote"

    def test_blockquote_children_string(self):
        """Test BlockQuote with a plain string child."""
        bq = BlockQuote("To be or not to be.")
        rendered = bq.render()
        assert rendered["children"] == ["To be or not to be."]

    def test_blockquote_children_component(self):
        """Test BlockQuote with a component child."""
        bq = BlockQuote(Text("Inner text"))
        rendered = bq.render()
        assert len(rendered["children"]) == 1
        assert rendered["children"][0]["type"] == "Text"

    def test_blockquote_children_list(self):
        """Test BlockQuote with a list of mixed children."""
        bq = BlockQuote(["First line", Text("Second line")])
        rendered = bq.render()
        assert len(rendered["children"]) == 2

    def test_blockquote_no_children(self):
        """Test BlockQuote with no children is valid."""
        bq = BlockQuote()
        rendered = bq.render()
        assert rendered["children"] == []

    def test_blockquote_cite_in_props(self):
        """Test cite is passed through props."""
        bq = BlockQuote("Quote", cite="Author Name")
        rendered = bq.render()
        assert rendered["props"]["cite"] == "Author Name"

    def test_blockquote_cite_none_by_default(self):
        """Test cite defaults to None."""
        bq = BlockQuote("Quote")
        rendered = bq.render()
        assert rendered["props"]["cite"] is None

    def test_blockquote_default_color(self):
        """Test color defaults to 'default'."""
        bq = BlockQuote("Quote")
        rendered = bq.render()
        assert rendered["props"]["color"] == "default"

    def test_blockquote_named_color_variants(self):
        """Test all named color variants are accepted."""
        for variant in ("default", "secondary", "destructive", "info", "success", "warning"):
            bq = BlockQuote("Quote", color=variant)
            rendered = bq.render()
            assert rendered["props"]["color"] == variant

    def test_blockquote_generic_css_color(self):
        """Test arbitrary CSS color values are passed through."""
        for css_color in ("blue", "#ff5733", "oklch(70% 0.2 240)", "rgb(100, 200, 50)"):
            bq = BlockQuote("Quote", color=css_color)
            rendered = bq.render()
            assert rendered["props"]["color"] == css_color

    def test_blockquote_icon_in_props(self):
        """Test icon name is in props."""
        bq = BlockQuote("Quote", icon="flame")
        rendered = bq.render()
        assert rendered["props"]["icon"] == "flame"

    def test_blockquote_icon_none_by_default(self):
        """Test icon defaults to None."""
        bq = BlockQuote("Quote")
        rendered = bq.render()
        assert rendered["props"]["icon"] is None

    def test_blockquote_icon_size_default(self):
        """Test icon_size defaults to 20."""
        bq = BlockQuote("Quote")
        rendered = bq.render()
        assert rendered["props"]["iconSize"] == 20

    def test_blockquote_icon_size_custom(self):
        """Test custom icon_size is serialised as iconSize."""
        bq = BlockQuote("Quote", icon="info", icon_size=32)
        rendered = bq.render()
        assert rendered["props"]["iconSize"] == 32

    def test_blockquote_class_name(self):
        """Test class_name is in props."""
        bq = BlockQuote("Quote", class_name="my-custom-class")
        rendered = bq.render()
        assert rendered["props"]["class_name"] == "my-custom-class"

    def test_blockquote_style(self):
        """Test style dict is in props."""
        bq = BlockQuote("Quote", style={"marginTop": "1rem"})
        rendered = bq.render()
        assert rendered["props"]["style"] == {"marginTop": "1rem"}

    def test_blockquote_custom_id(self):
        """Test custom id is preserved."""
        bq = BlockQuote("Quote", id="my-quote")
        rendered = bq.render()
        assert rendered["id"] == "my-quote"

    def test_blockquote_all_props_together(self):
        """Test BlockQuote with all props set at once."""
        bq = BlockQuote(
            "With great power comes great responsibility.",
            cite="Uncle Ben",
            color="destructive",
            icon="zap",
            icon_size=24,
            class_name="my-quote",
            id="hero-quote",
        )
        rendered = bq.render()
        assert rendered["type"] == "BlockQuote"
        assert rendered["id"] == "hero-quote"
        assert rendered["children"] == ["With great power comes great responsibility."]
        assert rendered["props"]["cite"] == "Uncle Ben"
        assert rendered["props"]["color"] == "destructive"
        assert rendered["props"]["icon"] == "zap"
        assert rendered["props"]["iconSize"] == 24
        assert rendered["props"]["class_name"] == "my-quote"
