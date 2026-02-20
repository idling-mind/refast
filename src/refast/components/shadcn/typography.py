"""Typography components."""

from typing import Any, Literal

from refast.components.base import Component


class Heading(Component):
    """
    Heading component for titles.

    Example:
        ```python
        Heading("Welcome", level=1)
        Heading("Section Title", level=2, class_name="text-blue-500")
        ```
    """

    component_type: str = "Heading"

    def __init__(
        self,
        text: str,
        level: Literal[1, 2, 3, 4, 5, 6] = 1,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.text = text
        self.level = level

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "level": self.level,
                "class_name": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": [self.text],
        }


class Paragraph(Component):
    """Paragraph text component."""

    component_type: str = "Paragraph"

    def __init__(
        self,
        text: str,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.text = text

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "class_name": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": [self.text],
        }


class Code(Component):
    """Code display component with optional syntax highlighting.

    Args:
        code: The code content to display.
        language: Programming language for syntax highlighting (e.g., 'python', 'javascript').
        inline: If True (default), renders as inline code. If False, renders as a code block.
        id: Optional component ID.
        class_name: Optional CSS class name.
    """

    component_type: str = "Code"

    def __init__(
        self,
        code: str,
        language: str | None = None,
        inline: bool = True,
        show_line_numbers: bool = False,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.show_line_numbers = show_line_numbers
        self.code = code
        self.language = language
        self.inline = inline

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "language": self.language,
                "inline": self.inline,
                "show_line_numbers": self.show_line_numbers,
                "class_name": self.class_name,
                "code": self.code,
                **self._serialize_extra_props(),
            },
            "children": [],
        }


class Link(Component):
    """Link component for navigation."""

    component_type: str = "Link"

    def __init__(
        self,
        text: str,
        href: str,
        target: Literal["_self", "_blank", "_parent", "_top"] = "_self",
        on_click: Any = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.text = text
        self.href = href
        self.target = target
        self.on_click = on_click

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "href": self.href,
                "target": self.target,
                "on_click": self.on_click.serialize() if self.on_click else None,
                "class_name": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": [self.text],
        }


class Markdown(Component):
    """
    Markdown component with GitHub Flavored Markdown (GFM) support.

    Renders Markdown content with GFM features including tables,
    strikethrough, task lists, and syntax-highlighted code blocks.

    Example:
        ```python
        Markdown(
            content=\"\"\"
            # Hello World

            This is **bold** and *italic* text.

            ```python
            print("Hello!")
            ```
            \"\"\",
        )
        ```

    Args:
        content: The Markdown content to render.
        allow_latex: Deprecated — LaTeX is now rendered server-side. Kept
            for backward compatibility; this parameter is ignored.
        allow_html: Whether to allow raw HTML in markdown (default False for security).
    """

    component_type: str = "Markdown"

    def __init__(
        self,
        content: str,
        allow_latex: bool = True,
        allow_html: bool = False,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name, **props)
        self.content = content
        self.allow_latex = allow_latex
        self.allow_html = allow_html

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "content": self.content,
                "allow_latex": self.allow_latex,
                "allow_html": self.allow_html,
                "class_name": self.class_name,
                **self._serialize_extra_props(),
            },
            "children": [],
        }
