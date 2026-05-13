"""Shared playground layout helper for component docs pages."""

from refast.components import (
    Card,
    CardContent,
    CardHeader,
    Column,
    Container,
    Row,
)


def playground_card(
    options: list,
    preview,
    code=None,
    title: str = "Interactive Playground",
    preview_class: str = "border rounded-lg p-6 bg-muted/30",
):
    """Return an Interactive Playground Card with a two-column layout.

    The component preview is on the left (flex-1) and the option controls
    are stacked in a column on the right (fixed width, shrinks cleanly).

    Args:
        options: List of Column widgets representing individual option controls.
        preview: The component (or Container) to preview.
        code: Optional Markdown widget with the live code snippet.
        title: Card header title (defaults to "Interactive Playground").
        preview_class: Tailwind classes for the preview wrapper Container.
    """
    content_children = [
        Row(
            gap=6,
            class_name="items-start",
            children=[
                # ── Left: preview area ─────────────────────────────────
                Container(
                    class_name=f"flex-1 min-w-0 {preview_class}",
                    children=preview if isinstance(preview, list) else [preview],
                ),
                # ── Right: stacked option controls ─────────────────────
                Column(
                    gap=4,
                    class_name="w-52 shrink-0",
                    children=options,
                ),
            ],
        ),
    ]

    if code is not None:
        content_children.append(code)

    return Card(
        children=[
            CardHeader(title=title),
            CardContent(children=content_children),
        ]
    )
