"""Tests for base component classes."""

from refast.components.base import Container, Fragment, Text


class TestComponent:
    """Tests for base Component class."""

    def test_component_has_id(self):
        """Test component generates a unique ID."""
        container = Container()
        assert container.id is not None
        assert len(container.id) > 0

    def test_component_custom_id(self):
        """Test component accepts custom ID."""
        container = Container(id="my-id")
        assert container.id == "my-id"

    def test_component_unique_ids(self):
        """Test each component gets a unique ID."""
        c1 = Container()
        c2 = Container()
        assert c1.id != c2.id

    def test_component_class_name(self):
        """Test component accepts class_name."""
        container = Container(class_name="my-class")
        assert container.class_name == "my-class"

    def test_component_style(self):
        """Test component accepts style dict."""
        container = Container(style={"color": "red"})
        assert container.style == {"color": "red"}

    def test_component_extra_props(self):
        """Test component accepts extra props."""
        container = Container(data_testid="test")
        assert container.extra_props == {"data_testid": "test"}

    def test_add_child_fluent(self):
        """Test add_child returns self for chaining."""
        container = Container()
        result = container.add_child(Text("A")).add_child(Text("B"))
        assert result is container
        assert len(container._children) == 2

    def test_add_children(self):
        """Test add_children adds multiple children."""
        container = Container()
        container.add_children([Text("A"), Text("B"), Text("C")])
        assert len(container._children) == 3

    def test_component_repr(self):
        """Test component repr."""
        container = Container(id="test-id")
        assert "Container" in repr(container)
        assert "test-id" in repr(container)


class TestContainer:
    """Tests for Container component."""

    def test_container_renders(self):
        """Test Container renders correctly."""
        container = Container(id="test", class_name="p-4")
        rendered = container.render()
        assert rendered["type"] == "Container"
        assert rendered["id"] == "test"
        assert rendered["props"]["class_name"] == "p-4"

    def test_container_with_children(self):
        """Test Container with children."""
        container = Container(
            children=[
                Text("Hello"),
                Text("World"),
            ]
        )
        rendered = container.render()
        assert len(rendered["children"]) == 2

    def test_container_renders_nested(self):
        """Test Container renders nested components."""
        container = Container(children=[Container(children=[Text("Nested")])])
        rendered = container.render()
        assert len(rendered["children"]) == 1
        assert rendered["children"][0]["type"] == "Container"

    def test_container_style_in_props(self):
        """Test Container includes style in props."""
        container = Container(style={"marginTop": "10px"})
        rendered = container.render()
        assert rendered["props"]["style"] == {"marginTop": "10px"}


class TestText:
    """Tests for Text component."""

    def test_text_renders_content(self):
        """Test Text renders content correctly."""
        text = Text("Hello")
        rendered = text.render()
        assert rendered["type"] == "Text"
        assert rendered["children"] == ["Hello"]

    def test_text_with_class_name(self):
        """Test Text with class_name."""
        text = Text("Hello", class_name="text-lg font-bold")
        rendered = text.render()
        assert rendered["props"]["class_name"] == "text-lg font-bold"

    def test_text_with_style(self):
        """Test Text with style."""
        text = Text("Hello", style={"color": "blue"})
        rendered = text.render()
        assert rendered["props"]["style"] == {"color": "blue"}


class TestFragment:
    """Tests for Fragment component."""

    def test_fragment_renders(self):
        """Test Fragment renders correctly."""
        fragment = Fragment([Text("A"), Text("B")])
        rendered = fragment.render()
        assert rendered["type"] == "Fragment"
        assert len(rendered["children"]) == 2

    def test_fragment_has_no_props(self):
        """Test Fragment has empty props."""
        fragment = Fragment([Text("A")])
        rendered = fragment.render()
        assert rendered["props"] == {}

    def test_fragment_empty(self):
        """Test Fragment with no children."""
        fragment = Fragment()
        rendered = fragment.render()
        assert rendered["children"] == []


class TestRenderChildren:
    """Tests for _render_children method."""

    def test_renders_component_children(self):
        """Test rendering Component children."""
        container = Container(children=[Text("Hello")])
        rendered = container.render()
        assert rendered["children"][0]["type"] == "Text"

    def test_renders_string_children(self):
        """Test rendering string children."""
        container = Container(children=["Hello", "World"])
        rendered = container.render()
        assert rendered["children"] == ["Hello", "World"]

    def test_renders_mixed_children(self):
        """Test rendering mixed children."""
        container = Container(children=[Text("A"), "plain text"])
        rendered = container.render()
        assert len(rendered["children"]) == 2
        assert rendered["children"][0]["type"] == "Text"
        assert rendered["children"][1] == "plain text"

    def test_renders_children_filters_none(self):
        """Test rendering filters out None children."""
        container = Container(children=[Text("A"), None, Text("B"), None])
        rendered = container.render()
        assert len(rendered["children"]) == 2
        assert rendered["children"][0]["type"] == "Text"
        assert rendered["children"][0]["children"] == ["A"]
        assert rendered["children"][1]["type"] == "Text"
        assert rendered["children"][1]["children"] == ["B"]

    def test_renders_children_filters_none_with_conditional(self):
        """Test rendering with conditional None pattern."""
        show_alert = False
        container = Container(
            children=[
                Text("Always shown"),
                Text("Conditional") if show_alert else None,
            ]
        )
        rendered = container.render()
        assert len(rendered["children"]) == 1
        assert rendered["children"][0]["children"] == ["Always shown"]
