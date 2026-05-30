"""Scroll-Stream Example — ScrollArea with sticky-bottom streaming Markdown.

Demonstrates:
- Streaming text into a Markdown component inside a ScrollArea
- `stick_to_bottom` prop: auto-scrolls to newest content unless the user
  has scrolled up; re-sticks when the user scrolls back to the bottom
- A toggle switch to enable / disable stick_to_bottom at runtime
- A "Stream More" button that appends additional random paragraphs

Run with:
    python app.py
Then open http://localhost:8000
"""

import asyncio
import random

from fastapi import FastAPI

from refast import Context, RefastApp
from refast.components import (
    Badge,
    Button,
    Card,
    CardContent,
    CardHeader,
    CardTitle,
    Column,
    Container,
    Heading,
    Label,
    Markdown,
    Row,
    ScrollArea,
    Separator,
    Switch,
    Text,
    ThemeSwitcher,
)

ui = RefastApp(title="Scroll-Stream Demo")

# ---------------------------------------------------------------------------
# Random text generation
# ---------------------------------------------------------------------------

_WORDS = (
    "the quick brown fox jumps over the lazy dog python streaming "
    "refast react async await component scroll sticky bottom live "
    "data token chunk paragraph heading list item code block output "
    "render update append prop websocket fastapi markdown syntax "
    "highlight bold italic inline link image table row column grid"
).split()

_TOPICS = [
    "Distributed Systems",
    "Real-time Data Pipelines",
    "Language Model Inference",
    "Reactive UI Patterns",
    "Async Python",
    "WebSocket Protocols",
    "Event-Driven Architecture",
    "Stream Processing",
    "Component Rendering",
    "State Management",
]

_CODE_SNIPPETS = [
    """\
```python
async def stream(ctx: Context):
    async for chunk in model.stream(prompt):
        await ctx.append_prop("output", "content", chunk)
```""",
    """\
```python
async def fetch_data(url: str) -> list[dict]:
    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        return r.json()
```""",
    """\
```python
@ui.page("/")
def home(ctx: Context):
    return ScrollArea(
        stick_to_bottom=ctx.state.get("sticky", True),
        class_name="h-[500px]",
        children=[Markdown(id="output", content="")],
    )
```""",
]


def _random_sentence(n: int = 12) -> str:
    return " ".join(random.choices(_WORDS, k=n)).capitalize() + "."


def _random_paragraph(sentences: int = 4) -> str:
    return " ".join(_random_sentence(random.randint(8, 16)) for _ in range(sentences))


def _random_chunk() -> str:
    """Return a random Markdown section (heading + body)."""
    topic = random.choice(_TOPICS)
    kind = random.randint(0, 3)

    if kind == 0:
        # Plain paragraphs
        return (
            f"\n\n## {topic}\n\n"
            + _random_paragraph()
            + "\n\n"
            + _random_paragraph()
        )
    elif kind == 1:
        # Bullet list
        items = "\n".join(f"- {_random_sentence(8)}" for _ in range(5))
        return f"\n\n## {topic}\n\n{items}"
    elif kind == 2:
        # Code block
        snippet = random.choice(_CODE_SNIPPETS)
        return f"\n\n## {topic}\n\n{_random_paragraph(2)}\n\n{snippet}"
    else:
        # Numbered list
        items = "\n".join(f"{i}. {_random_sentence(10)}" for i in range(1, 6))
        return f"\n\n## {topic}\n\n{items}"


# ---------------------------------------------------------------------------
# Callbacks
# ---------------------------------------------------------------------------


async def stream_more(ctx: Context):
    """Append a random section word-by-word to the Markdown output."""
    if ctx.state.get("streaming", False):
        return  # Prevent concurrent streams

    ctx.state.set("streaming", True)
    await ctx.update_props("stream-btn", {"disabled": True})
    await ctx.update_props("stream-status", {"variant": "default"})
    await ctx.update_text("stream-status", "Streaming…")

    section = _random_chunk()
    words = section.split(" ")

    for i, word in enumerate(words):
        chunk = word if i == 0 else " " + word
        await ctx.append_prop("markdown-output", "content", chunk)
        await asyncio.sleep(random.uniform(0.015, 0.06))

        if ctx.state.get("stop_requested", False):
            ctx.state.set("stop_requested", False)
            break

    ctx.state.set("streaming", False)
    await ctx.update_props("stream-btn", {"disabled": False})
    await ctx.update_props("stream-status", {"variant": "secondary"})
    await ctx.update_text("stream-status", "Ready")


async def stop_stream(ctx: Context):
    """Signal the running stream to stop."""
    ctx.state.set("stop_requested", True)


async def clear_output(ctx: Context):
    """Clear the Markdown content."""
    await ctx.update_props("markdown-output", {"content": ""})
    await ctx.update_text("stream-status", "Cleared")


async def toggle_sticky(ctx: Context):
    """Toggle stick_to_bottom on the ScrollArea."""
    print("Toggling sticky:", ctx.event_data)
    checked = ctx.event_data.get("value", True)
    ctx.state.set("sticky", checked)
    await ctx.update_props("scroll-area", {"stick_to_bottom": checked})


# ---------------------------------------------------------------------------
# Page
# ---------------------------------------------------------------------------


@ui.page("/")
def home(ctx: Context):
    sticky: bool = ctx.state.get("sticky", True)
    streaming: bool = ctx.state.get("streaming", False)

    return Container(
        class_name="max-w-3xl mx-auto py-8 px-4",
        children=[
            # ── Header ──────────────────────────────────────────────────
            Row(
                justify="between",
                align="center",
                class_name="mb-6",
                children=[
                    Column(
                        gap=1,
                        children=[
                            Heading("Scroll-Stream Demo"),
                            Text(
                                "Streaming Markdown inside a ScrollArea with sticky-bottom support",
                                class_name="text-muted-foreground",
                            ),
                        ],
                    ),
                    ThemeSwitcher(),
                ],
            ),
            # ── Controls card ────────────────────────────────────────────
            Card(
                class_name="mb-4",
                children=[
                    CardHeader(children=[CardTitle("Controls")]),
                    CardContent(
                        children=[
                            Row(
                                gap=3,
                                align="center",
                                class_name="flex-wrap",
                                children=[
                                    Button(
                                        "Stream More",
                                        id="stream-btn",
                                        on_click=ctx.callback(stream_more),
                                        variant="default",
                                        disabled=streaming,
                                    ),
                                    Button(
                                        "Stop",
                                        on_click=ctx.callback(stop_stream),
                                        variant="destructive",
                                    ),
                                    Button(
                                        "Clear",
                                        on_click=ctx.callback(clear_output),
                                        variant="outline",
                                    ),
                                    Separator(orientation="vertical", class_name="h-6"),
                                    # Sticky toggle
                                    Row(
                                        gap=2,
                                        align="center",
                                        children=[
                                            Switch(
                                                id="sticky-switch",
                                                on_checked_change=ctx.callback(toggle_sticky),
                                                default_checked=sticky,
                                            ),
                                            Label(
                                                "Stick to bottom",
                                                html_for="sticky-switch",
                                                class_name="cursor-pointer select-none",
                                            ),
                                        ],
                                    ),
                                    Badge(
                                        "Ready",
                                        id="stream-status",
                                        variant="secondary",
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
            # ── Output card ──────────────────────────────────────────────
            Card(
                children=[
                    CardHeader(children=[CardTitle("Output")]),
                    CardContent(
                        children=[
                            ScrollArea(
                                id="scroll-area",
                                class_name="border rounded-lg p-4 bg-muted/20",
                                style={"height": "500px"},
                                stick_to_bottom=sticky,
                                children=[
                                    Markdown(
                                        id="markdown-output",
                                        content=(
                                            "Click **Stream More** to append a random section.\n\n"
                                            "Toggle **Stick to bottom** to control auto-scrolling:\n\n"
                                            "- **On** — the view tracks new content automatically "
                                            "unless you scroll up\n"
                                            "- **Off** — scroll position is left entirely to you"
                                        ),
                                        class_name="prose-sm max-w-none",
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )


# ---------------------------------------------------------------------------
# ASGI app
# ---------------------------------------------------------------------------

app = FastAPI()
app.include_router(ui.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
