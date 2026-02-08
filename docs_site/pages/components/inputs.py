"""Form Inputs — /docs/components/inputs."""

from refast.components import Container, Heading, Markdown, Separator


PAGE_TITLE = "Form Inputs"
PAGE_ROUTE = "/docs/components/inputs"


def render(ctx):
    """Render the inputs reference page."""
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

## Components in this section

- **Input** — Text input field
- **Textarea** — Multi-line text area
- **Select** — Dropdown select with options
- **Checkbox** / **CheckboxGroup** — Single or grouped checkboxes
- **Radio** / **RadioGroup** — Radio button selection
- **Switch** — Toggle switch
- **Slider** — Range slider
- **DatePicker** — Date selection
- **Combobox** — Searchable select
- **InputOTP** / **InputOTPGroup** / **InputOTPSlot** / **InputOTPSeparator** — One-time password input
- **Form** / **FormField** — Form wrapper with validation support
- **Label** — Form field label

---

### Input

```python
Input(
    placeholder="Enter your name",
    value="",
    type="text",
    on_change=ctx.callback(handle_change),
    store_as="user_name",
)
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `placeholder` | `str` | `""` | Placeholder text |
| `value` | `str` | `""` | Current value |
| `type` | `"text" \| "email" \| "password" \| "number" \| ...` | `"text"` | Input type |
| `on_change` | `Callback \| None` | `None` | Change handler |
| `store_as` | `str \| None` | `None` | Client-side prop store key |
| `disabled` | `bool` | `False` | Disabled state |

---

### Select

```python
Select(
    options=[
        {"label": "Red", "value": "red"},
        {"label": "Blue", "value": "blue"},
    ],
    placeholder="Choose a color",
    on_value_change=ctx.callback(handle_select),
)
```

---

*See `AGENT_INSTRUCTIONS.md` for detailed content requirements per component.*
"""
