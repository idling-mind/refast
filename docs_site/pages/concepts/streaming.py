"""Streaming — /docs/concepts/streaming."""

from refast.components import Container, Heading, Markdown, Separator


PAGE_TITLE = "Streaming"
PAGE_ROUTE = "/docs/concepts/streaming"


def render(ctx):
    """Render the streaming concept page."""
    from docs_site.app import docs_layout

    content = Container(
        class_name="max-w-4xl mx-auto p-6",
        children=[
            Heading(PAGE_TITLE, level=1),
            Separator(class_name="my-4"),
            Markdown(content=CONTENT),
        ],
    )
    return docs_layout(ctx, content, PAGE_ROUTE)


CONTENT = r"""
> **TODO**: This page needs full content. See `AGENT_INSTRUCTIONS.md` in this folder.

## Overview

Streaming allows you to incrementally update a component's content, similar to how
ChatGPT streams its responses. It's ideal for LLM output, real-time logs, or any
content that arrives piece by piece.

## Basic Usage

```python
async def generate(ctx: Context):
    async with ctx.stream("output-text") as stream:
        for word in ["Hello", " ", "World", "!"]:
            await stream.send(word)
            await asyncio.sleep(0.1)
```

The target component needs an `id`:

```python
Text("", id="output-text")
```

## How It Works

1. `ctx.stream(target_id)` opens a streaming context
2. Each `stream.send(chunk)` appends text to the target component
3. The stream closes automatically when the `async with` block exits
4. The frontend accumulates chunks and renders them incrementally

## Streaming to Markdown

You can stream into a `Markdown` component for rich formatting:

```python
Markdown(content="", id="ai-response")

async def ask_ai(ctx: Context):
    async with ctx.stream("ai-response") as stream:
        async for chunk in ai_model.stream("Tell me about Python"):
            await stream.send(chunk)
```

## Performance Tips

- Use reasonable chunk sizes — very small chunks create overhead
- The frontend batches rapid updates for smooth rendering
- For chart data, consider `ctx.append_prop()` instead of streaming

## Next Steps

- [Background Jobs](/docs/concepts/background) — Long-running server tasks
- [DOM Updates](/docs/concepts/updates) — Other update methods
"""
