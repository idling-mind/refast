"""Tests for custom tags in Markdown component."""

import pytest
from pydantic import BaseModel, Field

from typing import Any
from refast.components.base import Component
from refast.components.shadcn.typography import Markdown
from refast.components.shadcn.button import Button
from refast.components.shadcn.card import Card


# Define mock components for testing
class CustomButton(Component):
    component_type = "CustomButton"

    def __init__(self, label: str, count: int = 1, active: bool = False):
        super().__init__()
        self.label = label
        self.count = count
        self.active = active

    def render(self):
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "label": self.label,
                "count": self.count,
                "active": self.active,
            },
            "children": [],
        }


class CustomSection(Component):
    component_type = "CustomSection"

    def __init__(self, title: str, children: Any = None):
        super().__init__()
        self.title = title
        self.add_children(children)

    def render(self):
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "title": self.title,
            },
            "children": self._render_children(),
        }


class CustomTextOnly(Component):
    component_type = "CustomTextOnly"

    def __init__(self, title: str, content: str):
        super().__init__()
        self.title = title
        self.content = content

    def render(self):
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "title": self.title,
                "content": self.content,
            },
            "children": [],
        }


class TestMarkdownCustomTags:
    """Tests for custom tags within Markdown component."""

    def test_self_closing_tag_basic(self):
        """Test basic self-closing tag rendering and Pydantic validation."""
        custom_tags = {"MyButton": CustomButton}
        content = "Click this button: <MyButton label=\"Submit\" count=\"5\" active=\"true\" />"
        
        md = Markdown(content=content, custom_tags=custom_tags)
        rendered = md.render()
        
        # Verify placeholder in content
        assert "/refast-component/" in rendered["props"]["content"]
        assert "![MyButton](/refast-component/" in rendered["props"]["content"]
        
        # Verify custom_components registration
        components = rendered["props"]["custom_components"]
        assert len(components) == 1
        
        comp_uuid = list(components.keys())[0]
        comp_data = components[comp_uuid]
        
        assert comp_data["type"] == "CustomButton"
        assert comp_data["props"]["label"] == "Submit"
        # Verify Pydantic coercion: string "5" coerced to int 5, "true" to bool True
        assert comp_data["props"]["count"] == 5
        assert comp_data["props"]["active"] is True

    def test_boolean_attribute_shorthand(self):
        """Test shorthand boolean attributes (e.g. active instead of active="true")."""
        custom_tags = {"MyButton": CustomButton}
        content = "Click <MyButton label=\"Shub\" active />"
        
        md = Markdown(content=content, custom_tags=custom_tags)
        rendered = md.render()
        
        components = rendered["props"]["custom_components"]
        comp_data = list(components.values())[0]
        assert comp_data["props"]["active"] is True

    def test_validation_failure_fallback(self):
        """Test that if validation fails, the tag is left as plain text."""
        custom_tags = {"MyButton": CustomButton}
        # Missing required attribute 'label'
        content = "Invalid: <MyButton count=\"abc\" />"
        
        md = Markdown(content=content, custom_tags=custom_tags)
        rendered = md.render()
        
        # No replacements should occur, content should be left as is
        assert rendered["props"]["content"] == content
        assert rendered["props"]["custom_components"] == {}

    def test_unregistered_tag_fallback(self):
        """Test that unregistered uppercase tags are left as is."""
        content = "Unknown: <SomeWidget value=\"123\" />"
        md = Markdown(content=content, custom_tags={})
        rendered = md.render()
        assert rendered["props"]["content"] == content

    def test_container_tag_children(self):
        """Test container tag that receives children as components."""
        custom_tags = {"Section": CustomSection}
        content = "<Section title=\"My Section\">Hello section text</Section>"
        
        md = Markdown(content=content, custom_tags=custom_tags)
        rendered = md.render()
        
        components = rendered["props"]["custom_components"]
        assert len(components) == 1
        
        comp_data = list(components.values())[0]
        assert comp_data["type"] == "CustomSection"
        assert comp_data["props"]["title"] == "My Section"
        
        # The inner content should be wrapped in a Markdown component
        assert len(comp_data["children"]) == 1
        child_md = comp_data["children"][0]
        assert child_md["type"] == "Markdown"
        assert child_md["props"]["content"] == "Hello section text"

    def test_container_tag_str_fallback(self):
        """Test container tag where parameter type is strictly string (so child fallback is used)."""
        custom_tags = {"TextOnly": CustomTextOnly}
        content = "<TextOnly title=\"Doc\">Strict text here</TextOnly>"
        
        md = Markdown(content=content, custom_tags=custom_tags)
        rendered = md.render()
        
        components = rendered["props"]["custom_components"]
        comp_data = list(components.values())[0]
        assert comp_data["type"] == "CustomTextOnly"
        assert comp_data["props"]["title"] == "Doc"
        # Should be passed as a plain string due to fallback
        assert comp_data["props"]["content"] == "Strict text here"

    def test_nested_tags_innermost_first(self):
        """Test nested tags are parsed inside-out (innermost processed first)."""
        custom_tags = {
            "Section": CustomSection,
            "MyButton": CustomButton,
        }
        content = "<Section title=\"Outer\">Click <MyButton label=\"Inner\" /> now</Section>"
        
        md = Markdown(content=content, custom_tags=custom_tags)
        rendered = md.render()
        
        components = rendered["props"]["custom_components"]
        # Outer Section and Inner MyButton should both be parsed
        assert len(components) == 2
        
        # Find MyButton and Section in the output
        btn_comp = [c for c in components.values() if c["type"] == "CustomButton"][0]
        sec_comp = [c for c in components.values() if c["type"] == "CustomSection"][0]
        
        assert btn_comp["props"]["label"] == "Inner"
        assert sec_comp["props"]["title"] == "Outer"
        
        # Verify the section child is Markdown containing the button placeholder
        sec_child_md = sec_comp["children"][0]
        assert sec_child_md["type"] == "Markdown"
        assert "/refast-component/" in sec_child_md["props"]["content"]
        assert "![MyButton](/refast-component/" in sec_child_md["props"]["content"]

    def test_child_traversal(self):
        """Test that custom components are returned in child traversal."""
        custom_tags = {"MyButton": CustomButton}
        content = "Click <MyButton label=\"Submit\" />"
        
        md = Markdown(content=content, custom_tags=custom_tags)
        
        # Pre-render traversal is empty because we haven't rendered (parsed) yet
        assert len(md._traversal_children()) == 0
        
        md.render()
        
        # Post-render traversal should contain the instantiated CustomButton
        traversed = md._traversal_children()
        assert len(traversed) == 1
        assert isinstance(traversed[0], CustomButton)
        assert traversed[0].label == "Submit"

    def test_literal_variant_validation(self):
        """Test that a Literal variant argument is validated and correctly coerced/parsed."""
        from typing import Literal
        from refast.components.shadcn.data_display import Badge

        def make_tag(label: str, variant: Literal["default", "secondary", "destructive", "outline", "success", "warning"] = "default"):
            return Badge(children=label, variant=variant)

        custom_tags = {"Tag": make_tag}
        
        # Test valid variant "success"
        content_success = "Success: <Tag label=\"Done!\" variant=\"success\" />"
        md = Markdown(content=content_success, custom_tags=custom_tags)
        rendered = md.render()
        components = rendered["props"]["custom_components"]
        assert len(components) == 1
        comp_data = list(components.values())[0]
        assert comp_data["type"] == "Badge"
        assert comp_data["props"]["variant"] == "success"

        # Test invalid variant "invalid_variant"
        content_invalid = "Invalid: <Tag label=\"Done!\" variant=\"invalid_variant\" />"
        md_invalid = Markdown(content=content_invalid, custom_tags=custom_tags)
        rendered_invalid = md_invalid.render()
        # Should fall back to raw text because validation failed
        assert rendered_invalid["props"]["content"] == content_invalid
        assert rendered_invalid["props"]["custom_components"] == {}

