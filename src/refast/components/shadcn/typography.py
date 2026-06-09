import inspect
import re
from collections.abc import Callable
from typing import Any, Literal

from pydantic import validate_call

from refast.components.base import ChildrenType, Component


def _validate_and_call(callable_obj: Any, kwargs: dict[str, Any]) -> Any:
    """Validate arguments and invoke function/class constructor using Pydantic."""
    if isinstance(callable_obj, type):
        validated_init = validate_call(callable_obj.__init__)
        instance = callable_obj.__new__(callable_obj)
        validated_init(instance, **kwargs)
        return instance
    else:
        validated_func = validate_call(callable_obj)
        return validated_func(**kwargs)


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
        style: dict[str, Any] | None = None,
        parent_style: dict[str, Any] | None = None,
        extra_props: dict[str, Any] | None = None,
    ):
        super().__init__(
            id=id,
            class_name=class_name,
            style=style,
            parent_style=parent_style,
            extra_props=extra_props,
        )
        self.text = text
        self.level = level
        self.style = style

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "level": self.level,
                "class_name": self.class_name,
                "style": self.style,
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
        lead: bool = False,
        muted: bool = False,
        id: str | None = None,
        class_name: str = "",
        style: dict[str, Any] | None = None,
        parent_style: dict[str, Any] | None = None,
        extra_props: dict[str, Any] | None = None,
    ):
        super().__init__(
            id=id,
            class_name=class_name,
            style=style,
            parent_style=parent_style,
            extra_props=extra_props,
        )
        self.text = text
        self.lead = lead
        self.muted = muted
        self.style = style

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "lead": self.lead,
                "muted": self.muted,
                "class_name": self.class_name,
                "style": self.style,
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
        style: Optional inline styles as a dictionary.
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
        style: dict[str, Any] | None = None,
        parent_style: dict[str, Any] | None = None,
        extra_props: dict[str, Any] | None = None,
    ):
        super().__init__(
            id=id,
            class_name=class_name,
            style=style,
            parent_style=parent_style,
            extra_props=extra_props,
        )
        self.show_line_numbers = show_line_numbers
        self.code = code
        self.language = language
        self.style = style
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
                "style": self.style,
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
        external: bool = False,
        id: str | None = None,
        class_name: str = "",
        style: dict[str, Any] | None = None,
        parent_style: dict[str, Any] | None = None,
        extra_props: dict[str, Any] | None = None,
    ):
        super().__init__(
            id=id,
            class_name=class_name,
            style=style,
            parent_style=parent_style,
            extra_props=extra_props,
        )
        self.text = text
        self.href = href
        self.target = target
        self.external = external
        self.style = style
        self.on_click = on_click

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "href": self.href,
                "target": self.target,
                "external": self.external,
                "on_click": self.on_click.serialize() if self.on_click else None,
                "class_name": self.class_name,
                "style": self.style,
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
        allow_html: Whether to allow raw HTML in markdown (default False for security).
        enable_mermaid: Enable Mermaid diagram rendering for fenced ```mermaid blocks.
            The Mermaid library is loaded on demand only when this is True.
        enable_latex: Enable LaTeX / KaTeX math rendering ($..$ and $$..$$).
            The KaTeX library is loaded on demand only when this is True.
        custom_tags: A dictionary mapping tag names (str) to callables that return a component.
        custom_components: A dictionary mapping component IDs (str) to serialized component
            trees (for internal use).
    """

    component_type: str = "Markdown"

    def __init__(
        self,
        content: str,
        allow_html: bool = False,
        enable_mermaid: bool = False,
        enable_latex: bool = False,
        custom_tags: dict[str, Callable[..., Component]] | None = None,
        custom_components: dict[str, Any] | None = None,
        id: str | None = None,
        class_name: str = "",
        style: dict[str, Any] | None = None,
        parent_style: dict[str, Any] | None = None,
        extra_props: dict[str, Any] | None = None,
    ):
        super().__init__(
            id=id,
            class_name=class_name,
            style=style,
            parent_style=parent_style,
            extra_props=extra_props,
        )
        self.content = content
        self.allow_html = allow_html
        self.enable_mermaid = enable_mermaid
        self.enable_latex = enable_latex
        self.style = style
        self.custom_tags = custom_tags or {}
        self.custom_components = dict(custom_components) if custom_components else {}

    def _parse_custom_tags(self) -> str:
        if not self.custom_tags:
            return self.content

        content = self.content
        tag_counts = {}

        # Innermost first parsing loop
        # We search for self-closing or container tags matching <[A-Z]
        self_closing_rx = re.compile(r'<([A-Z][a-zA-Z0-9_]*)(?:\s+([^>]*?))?\s*\/>')
        container_rx = re.compile(r'<([A-Z][a-zA-Z0-9_]*)(?:\s+([^>]*?))?\s*>(.*?)</\1>', re.DOTALL)

        def parse_attributes(attrs_str: str) -> dict[str, Any]:
            if not attrs_str:
                return {}
            attr_rx = re.compile(
                r'([a-zA-Z0-9_-]+)(?:\s*=\s*(?:"([^"]*)"|\'([^\']*)\'|([^\s>]+)))?'
            )
            attrs = {}
            for match in attr_rx.finditer(attrs_str):
                name = match.group(1)
                val_group = match.group(0)
                if '=' in val_group:
                    val = match.group(2) or match.group(3) or match.group(4) or ""
                else:
                    val = True
                attrs[name] = val
            return attrs

        while True:
            # 1. Try to find the first self-closing tag
            match = self_closing_rx.search(content)
            if match:
                tag_name = match.group(1)
                attrs_str = match.group(2)

                if tag_name in self.custom_tags:
                    attrs = parse_attributes(attrs_str)
                    try:
                        instance = _validate_and_call(self.custom_tags[tag_name], attrs)
                        tag_counts[tag_name] = tag_counts.get(tag_name, 0) + 1
                        comp_id = f"{tag_name}_{tag_counts[tag_name]}"
                        self.custom_components[comp_id] = instance
                        replacement = f"![{tag_name}](/refast-component/{comp_id})"
                        content = content[:match.start()] + replacement + content[match.end():]
                    except Exception:
                        # Validation failed (or other error), leave tag text
                        # as is (mark temporarily)
                        failed_marker = f"<__FAILED_SELF_{tag_name} {attrs_str or ''} />"
                        content = content[:match.start()] + failed_marker + content[match.end():]
                else:
                    # Tag name not registered in custom_tags, leave it as is
                    failed_marker = f"<__FAILED_SELF_{tag_name} {attrs_str or ''} />"
                    content = content[:match.start()] + failed_marker + content[match.end():]
                continue

            # 2. Try to find the first container tag with no nested un-processed tags.
            # We iterate through container tag matches.
            container_match = None
            for m in container_rx.finditer(content):
                inner_text = m.group(3)
                # If inner_text contains '<[A-Z]', there is an inner un-processed tag. Skip for now.
                # Note: we exclude '<__FAILED_' markers as they are already processed/failed.
                # So we search for '<' followed by an uppercase letter: '<[A-Z]'
                if re.search(r'<[A-Z]', inner_text):
                    continue
                container_match = m
                break

            if container_match:
                tag_name = container_match.group(1)
                attrs_str = container_match.group(2)
                inner_content = container_match.group(3)

                if tag_name in self.custom_tags:
                    attrs = parse_attributes(attrs_str)
                    callable_obj = self.custom_tags[tag_name]

                    # Check signature to see if it accepts children/content
                    if isinstance(callable_obj, type):
                        sig = inspect.signature(callable_obj.__init__)
                        params = list(sig.parameters.keys())
                        if 'self' in params:
                            params.remove('self')
                    else:
                        sig = inspect.signature(callable_obj)
                        params = list(sig.parameters.keys())

                    param_name = None
                    if 'children' in params:
                        param_name = 'children'
                    elif 'content' in params:
                        param_name = 'content'

                    try:
                        if param_name:
                            # Try to pass inner_content wrapped as Markdown component
                            child_markdown = Markdown(
                                content=inner_content,
                                allow_html=self.allow_html,
                                enable_mermaid=self.enable_mermaid,
                                enable_latex=self.enable_latex,
                                custom_tags=self.custom_tags,
                                custom_components=self.custom_components,
                            )
                            attrs_with_child = dict(attrs)
                            attrs_with_child[param_name] = child_markdown
                            try:
                                instance = _validate_and_call(callable_obj, attrs_with_child)
                            except Exception:
                                # Fall back to passing raw inner_content as a
                                # string (e.g. if type is strictly str)
                                attrs_with_child[param_name] = inner_content
                                instance = _validate_and_call(callable_obj, attrs_with_child)
                        else:
                            instance = _validate_and_call(callable_obj, attrs)

                        tag_counts[tag_name] = tag_counts.get(tag_name, 0) + 1
                        comp_id = f"{tag_name}_{tag_counts[tag_name]}"
                        self.custom_components[comp_id] = instance
                        replacement = f"![{tag_name}](/refast-component/{comp_id})"
                        content = (
                            content[:container_match.start()]
                            + replacement
                            + content[container_match.end():]
                        )
                    except Exception:
                        failed_marker = (
                            f"<__FAILED_CONT_{tag_name} {attrs_str or ''}>"
                            f"{inner_content}</__FAILED_CONT_{tag_name}>"
                        )
                        content = (
                            content[:container_match.start()]
                            + failed_marker
                            + content[container_match.end():]
                        )
                else:
                    failed_marker = (
                        f"<__FAILED_CONT_{tag_name} {attrs_str or ''}>"
                        f"{inner_content}</__FAILED_CONT_{tag_name}>"
                    )
                    content = (
                        content[:container_match.start()]
                        + failed_marker
                        + content[container_match.end():]
                    )
                continue

            # If no self-closing or container matches can be processed, we are done!
            break

        # Restore failed markers back to their original tags
        content = (
            content.replace("<__FAILED_SELF_", "<")
            .replace("<__FAILED_CONT_", "<")
            .replace("</__FAILED_CONT_", "</")
        )
        return content

    def _traversal_children(self) -> "list[Component]":
        children = super()._traversal_children()
        if hasattr(self, 'custom_components') and self.custom_components:
            for comp in self.custom_components.values():
                if isinstance(comp, Component):
                    children.append(comp)
        return children

    def render(self) -> dict[str, Any]:
        processed_content = self._parse_custom_tags()
        serialized_components = {}
        for k, v in self.custom_components.items():
            if hasattr(v, "render"):
                serialized_components[k] = v.render()
            else:
                serialized_components[k] = v

        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "content": processed_content,
                "allow_html": self.allow_html,
                "enable_mermaid": self.enable_mermaid,
                "enable_latex": self.enable_latex,
                "class_name": self.class_name,
                "style": self.style,
                "custom_components": serialized_components,
                **self._serialize_extra_props(),
            },
            "children": [],
        }


class BlockQuote(Component):
    """
    Blockquote component for styled quoted text with optional icon and citation.

    Example:
        ```python
        BlockQuote(
            "To be or not to be, that is the question.",
            cite="Hamlet, Shakespeare",
            color="default",
            icon="quote",
            icon_size=20,
        )
        BlockQuote(
            "Premature optimisation is the root of all evil.", cite="Donald Knuth", color="info"
        )
        BlockQuote(
            "With great power comes great responsibility.", color="destructive", icon="zap"
        )
        ```

    Args:
        children: The quoted text or child components to display as the quote body.
        cite: Optional attribution text displayed below the quote (e.g., author name).
        color: Color variant for the background and left border. Named options:
               "default", "secondary", "destructive", "info", "success", "warning".
               Also accepts any CSS color value (e.g., "blue", "#ff0000", "oklch(…)").
        icon: Optional Lucide icon name to display at the top of the quote
              (e.g., "quote", "flame", "info", "zap"). Uses the same icon names
              as the ``Icon`` component.
        icon_size: Size of the icon in pixels (default: 20).
        id: Optional component ID.
        class_name: Optional CSS class name.
        style: Optional inline styles as a dictionary.
    """

    component_type: str = "BlockQuote"

    def __init__(
        self,
        children: "ChildrenType" = None,
        cite: str | None = None,
        color: str = "default",
        icon: str | None = None,
        icon_size: int = 20,
        id: str | None = None,
        class_name: str = "",
        style: dict[str, Any] | None = None,
        parent_style: dict[str, Any] | None = None,
        extra_props: dict[str, Any] | None = None,
    ):
        super().__init__(
            id=id,
            class_name=class_name,
            style=style,
            parent_style=parent_style,
            extra_props=extra_props,
        )
        self.add_children(children)
        self.cite = cite
        self.color = color
        self.icon = icon
        self.icon_size = icon_size
        self.style = style

    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "cite": self.cite,
                "color": self.color,
                "icon": self.icon,
                "iconSize": self.icon_size,
                "class_name": self.class_name,
                "style": self.style,
                **self._serialize_extra_props(),
            },
            "children": self._render_children(),
        }
