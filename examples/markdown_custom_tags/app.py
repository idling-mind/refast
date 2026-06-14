"""Markdown Custom Tags Showcase example.

Demonstrates:
- Embedding custom Refast components inline inside Markdown content.
- Using Pydantic to validate and coerce tag arguments.
- Handling callbacks, state persistence, and dynamic page re-renders.
- Streaming Markdown with custom components in real-time.

Run this file with:
    python app.py
or using your local venv python:
    .venv/Scripts/python examples/markdown_custom_tags/app.py
"""

import asyncio
from typing import Any, Literal

from fastapi import FastAPI

from refast import Context, RefastApp
from refast.components import (
    Badge,
    Button,
    Calendar,
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
    Container,
    Heading,
    Markdown,
    Progress,
    Row,
    ThemeSwitcher,
)

ui = RefastApp(title="Markdown Custom Tags Showcase")


# Callbacks
async def increment_counter(ctx: Context):
    """Increment the progress value and show a toast."""
    current = ctx.store.local.get("progress_val", 30)
    new_val = min(100, current + 10)
    # Reset to 0 if we hit 100
    if new_val == 100:
        new_val = 0
    ctx.store.local["progress_val"] = new_val
    await ctx.show_toast(f"Progress updated: {new_val}%", variant="success")
    await ctx.update_props(
        "progress-bar", {"value": new_val}
    )


async def on_date_select(ctx: Context, value: str = ""):
    """Save selected date from the calendar and refresh."""
    # Slice the ISO timestamp to just the date: YYYY-MM-DD
    date_str = value[:10] if value else "None"
    ctx.store.local["selected_date"] = date_str
    await ctx.show_toast(f"Date selected: {date_str}", variant="info")
    await ctx.refresh()


async def stream_markdown_with_tags(ctx: Context):
    """Simulate streaming markdown with custom components inline."""
    # Reset/clear previous content and status
    await ctx.update_props(
        "streaming-output",
        {"content": "Starting stream...", "custom_components": {}},
    )
    await ctx.show_toast("Streaming starting...", variant="info")

    # Define custom tag factory functions capturing ctx via closure
    def make_tag(
        label: str,
        variant: Literal[
            "default", "secondary", "destructive", "outline", "success", "warning"
        ] = "default",
    ):
        return Badge(children=label, variant=variant)

    def make_button(label: str, variant: str = "default"):
        return Button(
            label,
            variant=variant,
            on_click=ctx.callback(increment_counter)
        )

    def make_progress(id: str, value: int = 0):
        return Progress(id=id, value=value, class_name="w-full max-w-md my-2")

    def make_button_row(children: Any):
        return Row(
            class_name="flex flex-row gap-2 items-center p-2 border rounded bg-muted/10 my-2",
            children=children
        )

    custom_tags = {
        "Tag": make_tag,
        "CounterButton": make_button,
        "ProgressBar": make_progress,
        "ButtonRow": make_button_row,
    }

    chunks = [
        "## Real-time Streaming of Custom Components\n\n",
        "We can stream text chunk-by-chunk. Unfinished HTML tags are displayed as plain text, ",
        "but as soon as a tag becomes complete, Refast parses and renders it reactively!\n\n",
        "Here is a status label: <Tag label=\"Streaming...\" variant=\"secondary\" />\n\n",
        "Let's add a progress bar at 40%: ",
        "<ProgressBar id=\"progress-bar\" value=\"40\" />\n\n",
        "We can also stream buttons with callback actions: "
        "<CounterButton label=\"Increment progress\" />\n\n",
        "We can also stream container tags containing multiple components:\n",
        "<ButtonRow>\n",
        "  <CounterButton label=\"Row Button 1\" variant=\"outline\" />\n",
        "  <CounterButton label=\"Row Button 2\" variant=\"secondary\" />\n",
        "</ButtonRow>\n\n",
        "And another tag at the end: <Tag label=\"Stream Finished!\" variant=\"success\" />\n"
    ]

    current_text = ""
    for chunk in chunks:
        current_text += chunk

        # Instantiate a temporary Markdown component to run parsing and validation
        temp_md = Markdown(content=current_text, custom_tags=custom_tags)
        rendered = temp_md.render()

        # Update client props in a single call (sending both the parsed content
        # and serialized child components)
        await ctx.update_props("streaming-output", {
            "content": rendered["props"]["content"],
            "custom_components": rendered["props"]["custom_components"]
        })

        # Delay to simulate network / generation latency
        await asyncio.sleep(0.2)

    await ctx.show_toast("Streaming complete!", variant="success")


@ui.page("/")
def index(ctx: Context):
    # Initialize states if not present
    if "progress_val" not in ctx.store.local:
        ctx.store.local["progress_val"] = 30
    if "selected_date" not in ctx.store.local:
        ctx.store.local["selected_date"] = "2026-06-09"

    progress_val = ctx.store.local["progress_val"]
    selected_date = ctx.store.local["selected_date"]

    # Define custom tag factory functions in page scope to capture ctx via closure
    def make_tag(
        label: str,
        variant: Literal[
            "default", "secondary", "destructive", "outline", "success", "warning"
        ] = "default",
    ):
        return Badge(children=label, variant=variant)

    def make_button(label: str, variant: str = "default"):
        return Button(
            label,
            variant=variant,
            on_click=ctx.callback(increment_counter)
        )

    def make_progress(id: str, value: int = 0):
        return Progress(id=id, value=value, class_name="w-full max-w-md my-2")

    def make_calendar(id: str, selected_date: str | None = None):
        return Calendar(
            id=id,
            mode="single",
            selected=selected_date,
            on_select=ctx.callback(on_date_select)
        )

    def make_button_row(children: Any):
        return Row(
            class_name="flex flex-row gap-2 items-center p-2 border rounded bg-muted/10 my-2",
            children=children
        )

    # Dictionary of custom tags mapped to their Pydantic-validated constructors/factories
    custom_tags = {
        "Tag": make_tag,
        "CounterButton": make_button,
        "ProgressBar": make_progress,
        "DatePickerCalendar": make_calendar,
        "ButtonRow": make_button_row,
    }

    # Markdown template containing custom tags
    markdown_content = f"""# Markdown Custom Tags Showcase

This example demonstrates how to integrate **interactive Refast components**
directly inside standard Markdown text blocks using HTML-like tags.

Under the hood:
1. The backend parses custom tags (e.g. `<Tag />`, `<ProgressBar />`).
2. Arguments are validated and coerced (e.g. string numbers to float/int) using **Pydantic**.
3. Registered components are serialized and rendered **inline** inside the
   markdown flow on the client.

---

### 1. Custom Tags (`<Tag />` -> `Badge`)
Embed labels directly in your text:
* This is a <Tag label="Stable" variant="default" /> release.
* A critical warning: <Tag label="Deprecation Notice" variant="destructive" /> is active.
* Here is an outline tag: <Tag label="v1.2.0" variant="outline" />

---

### 2. Button Callback (`<CounterButton />` -> `Button`)
Click the button below to trigger a Python callback and update the page state:

<CounterButton label="Click to Increment Progress" variant="secondary" />

*Current Value: **{progress_val}%*** (Clicking increments by 10%, resets at 100%)

---

### 3. Progress Bar (`<ProgressBar />` -> `Progress`)
The tag below binds its value argument directly to the current state:

<ProgressBar id="progress-bar" value="{progress_val}" />

---

### 4. Interactive Calendar (`<DatePickerCalendar />` -> `Calendar`)
Select a date below to fire a callback, update local store, and refresh the text:

<DatePickerCalendar id="date-picker" selected_date="{selected_date}" />

Selected Date in State: **{selected_date}**

---

### 5. Container Tag (`<ButtonRow>...</ButtonRow>` -> `Row`)
Group multiple interactive elements horizontally using a container tag:

<ButtonRow>
  <CounterButton label="Row Button A" variant="outline" />
  <CounterButton label="Row Button B" variant="secondary" />
  <CounterButton label="Row Button C" variant="default" />
</ButtonRow>

---

### 6. Code Blocks & Syntax Highlighting
Here are code blocks rendered in different programming languages:

**Python:**
```python
def greet(name: str) -> None:
    print("Hello", name)

greet("Refast developer")
```

**JavaScript:**
```javascript
const colors = ["red", "green", "blue"];
const upperColors = colors.map(c => c.toUpperCase());
console.log(upperColors);
```

**Bash / Shell:**
```bash
# Start the Refast application dev server
python examples/markdown_custom_tags/app.py
```
"""

    return Container(
        class_name="p-6 max-w-4xl mx-auto space-y-6",
        children=[
            Row(
                class_name="justify-between items-center",
                children=[
                    Heading("Markdown Custom Tags", level=1),
                    ThemeSwitcher(),
                ]
            ),
            # Showcase card
            Card(
                children=[
                    CardHeader(
                        children=[
                            CardTitle("Rich Content Showcase"),
                            CardDescription(
                                "Refast components rendered inline within Markdown "
                                "using standard HTML-like syntax"
                            ),
                        ]
                    ),
                    CardContent(
                        children=[
                            Markdown(
                                content=markdown_content,
                                custom_tags=custom_tags,
                            )
                        ]
                    )
                ]
            ),
            # Streaming card
            Card(
                children=[
                    CardHeader(
                        children=[
                            CardTitle("Streaming Showcase"),
                            CardDescription(
                                "Demonstrates dynamic token-by-token streaming of "
                                "Markdown containing interactive components"
                            ),
                        ]
                    ),
                    CardContent(
                        class_name="space-y-4",
                        children=[
                            Button(
                                "Start Streaming Tagged Content",
                                on_click=ctx.callback(stream_markdown_with_tags),
                            ),
                            Container(
                                class_name="min-h-[250px] p-4 border rounded-lg bg-muted/20",
                                children=[
                                    Markdown(
                                        id="streaming-output",
                                        content="Click the button above to begin streaming...",
                                    )
                                ]
                            )
                        ]
                    )
                ]
            )
        ]
    )


app = FastAPI()
app.include_router(ui.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
