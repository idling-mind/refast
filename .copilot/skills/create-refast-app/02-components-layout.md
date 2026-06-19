# Refast — Components & Layout Reference

All components are importable from `refast.components`:

```python
from refast import components as rc          # namespace import
from refast.components import Button, Row, Column, Text  # named imports
```

Every component accepts these universal kwargs:
- `id: str | None` — used for targeting with `ctx.replace()`, `ctx.append()`, etc.
- `class_name: str` — Tailwind CSS utility classes
- `style: dict` — inline CSS dict with camelCase keys (React style)
- `children: list | Any` — child components or strings. `None` values in lists are silently filtered.
- `extra_props: dict` — pass arbitrary HTML/React props through

---

## Children Pattern

`children` accepts a single component, a string, or a list. `None` in lists is filtered — useful for conditionals:

```python
rc.Column(children=[
    rc.Alert(title="Error", variant="destructive") if errors else None,  # filtered if None
    rc.Input(name="email"),
    rc.Button("Submit"),
])
```

---

## 1. Base / Primitive Components

### `Container`

**Signature:**
```python
rc.Container(children: ChildrenType = None, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)
```
Generic `<div>` wrapper. Add Tailwind via `class_name`.
```python
rc.Container(
    id="main",
    class_name="p-4 bg-background max-w-4xl mx-auto",
    style={"maxWidth": "72rem"},
    children=[...],
)
```

### `Text`

**Signature:**
```python
rc.Text(content: str, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)
```
Inline text span.
```python
rc.Text("Hello!", class_name="text-sm font-medium text-muted-foreground")
```

### `Fragment`

**Signature:**
```python
rc.Fragment(children: ChildrenType = None)
```
Groups children with no DOM wrapper.
```python
rc.Fragment([rc.Text("Line 1"), rc.Text("Line 2")])
```

---

## 2. Layout Components

### `Row`

**Signature:**
```python
rc.Row(children: ChildrenType = None, justify: Literal['start', 'end', 'center', 'between', 'around', 'evenly'] = 'start', align: Literal['start', 'end', 'center', 'stretch', 'baseline'] = 'start', gap: int = 2, wrap: bool = False, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)
```
Horizontal flex container.
```python
rc.Row(
    children=[rc.Button("A"), rc.Button("B")],
    justify="between",   # "start"|"end"|"center"|"between"|"around"|"evenly"
    align="center",      # "start"|"end"|"center"|"stretch"|"baseline"
    gap=4,               # Tailwind spacing integer (×0.25rem)
    wrap=False,
    class_name="w-full",
)
```

### `Column`

**Signature:**
```python
rc.Column(children: ChildrenType = None, justify: Literal['start', 'end', 'center', 'between', 'around', 'evenly'] = 'start', align: Literal['start', 'end', 'center', 'stretch', 'baseline'] = 'stretch', gap: int = 2, wrap: bool = False, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)
```
Vertical flex container. Same props as `Row`.
```python
rc.Column(
    children=[rc.Text("Line 1"), rc.Text("Line 2")],
    gap=2,
    align="stretch",
)
```

### `Grid`

**Signature:**
```python
rc.Grid(children: ChildrenType = None, columns: int | str = 1, rows: int | str | None = None, gap: int = 4, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)
```
CSS Grid container.
```python
rc.Grid(
    children=[rc.Card(...) for _ in range(6)],
    columns=3,           # int or CSS string like "1fr 2fr"
    rows=None,           # int or CSS string; None = auto
    gap=4,
)
```

### `Flex`

**Signature:**
```python
rc.Flex(children: ChildrenType = None, direction: Literal['row', 'column', 'row-reverse', 'column-reverse'] = 'row', justify: Literal['start', 'end', 'center', 'between', 'around', 'evenly'] = 'start', align: Literal['start', 'end', 'center', 'stretch', 'baseline'] = 'stretch', wrap: bool = False, gap: int = 2, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)
```
Full directional flexbox (row/column/reverse). Use `Row`/`Column` for most cases.
```python
rc.Flex(
    direction="row-reverse",   # "row"|"column"|"row-reverse"|"column-reverse"
    justify="between",
    align="center",
    wrap=True,
    gap=2,
    children=[...],
)
```

### `Center`

**Signature:**
```python
rc.Center(children: ChildrenType = None, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)
```
Centers children both horizontally and vertically.
```python
rc.Center(
    class_name="h-screen",
    children=[rc.Heading("Welcome", level=1)],
)
```

---

## 3. Typography Components

### `Heading`

**Signature:**
```python
rc.Heading(text: str, level: Literal[1, 2, 3, 4, 5, 6] = 1, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)
```
```python
rc.Heading("Welcome", level=1)            # level: 1–6
rc.Heading("Section", level=2, class_name="text-blue-500")
```

### `Paragraph`

**Signature:**
```python
rc.Paragraph(text: str, lead: bool = False, muted: bool = False, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)
```
```python
rc.Paragraph("Regular text.")
rc.Paragraph("Lead paragraph.", lead=True)     # larger/emphasized
rc.Paragraph("Muted note.", muted=True)        # muted-foreground color
```

### `Code`

**Signature:**
```python
rc.Code(code: str, language: str | None = None, inline: bool = True, show_line_numbers: bool = False, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)
```
```python
rc.Code(code="print('hello')", language="python", inline=False, show_line_numbers=True)
rc.Code(code="x = 1", inline=True)   # inline code span
```

### `Link`

**Signature:**
```python
rc.Link(text: str | None = None, href: str = '#', children: ChildrenType = None, variant: Literal['default', 'unstyled'] = 'default', target: Literal['_self', '_blank', '_parent', '_top'] = '_self', on_click: Any = None, external: bool = False, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)
```
```python
rc.Link(text="Visit Docs", href="/docs", target="_self")
rc.Link(text="GitHub", href="https://github.com", external=True, target="_blank")
```

### `BlockQuote`

**Signature:**
```python
rc.BlockQuote(children: ChildrenType = None, cite: str | None = None, color: str = 'default', icon: str | None = None, icon_size: int = 20, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)
```
```python
rc.BlockQuote(children=[rc.Text("The only way to do great work is to love what you do.")])
```

### `Markdown`

**Signature:**
```python
rc.Markdown(content: str, allow_html: bool = False, enable_mermaid: bool = False, enable_latex: bool = False, custom_tags: dict[str, collections.abc.Callable[..., refast.components.base.Component]] | None = None, custom_components: dict[str, Any] | None = None, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)
```
Renders a Markdown string as rich HTML. Requires `preloaded_features=["markdown"]`.
```python
rc.Markdown("# Hello\n\nThis is **bold** and _italic_.")
rc.Markdown(id="output", content="")   # start empty for streaming
```

### `Separator`

**Signature:**
```python
rc.Separator(orientation: Literal['horizontal', 'vertical'] = 'horizontal', decorative: bool = True, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)
```
```python
rc.Separator()                              # horizontal divider
rc.Separator(orientation="vertical", class_name="h-6")
```

---

## 4. Button Components

### `Button`

**Signature:**
```python
rc.Button(label: str, variant: Literal['default', 'secondary', 'destructive', 'outline', 'ghost', 'link'] = 'default', size: Literal['xs', 'sm', 'md', 'lg', 'xl'] = 'md', icon: str | None = None, icon_position: Literal['left', 'right'] = 'left', disabled: bool = False, loading: bool = False, type: Literal['button', 'submit', 'reset'] = 'button', on_click: Any = None, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)
```
```python
rc.Button(
    label="Click Me",
    variant="default",       # "default"|"secondary"|"destructive"|"outline"|"ghost"|"link"
    size="md",               # "xs"|"sm"|"md"|"lg"|"xl"
    icon="save",             # Lucide icon name (optional)
    icon_position="left",    # "left"|"right"
    disabled=False,
    loading=False,           # shows spinner, disables button
    type="button",           # "button"|"submit"|"reset"
    on_click=ctx.callback(handler),
)
```

### `IconButton`

**Signature:**
```python
rc.IconButton(icon: str, variant: Literal['default', 'secondary', 'destructive', 'outline', 'ghost'] = 'ghost', size: Literal['xs', 'sm', 'md', 'lg', 'xl'] = 'md', disabled: bool = False, on_click: Any = None, aria_label: str | None = None, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)
```
Square icon-only button.
```python
rc.IconButton(
    icon="trash",
    variant="ghost",
    size="md",
    disabled=False,
    aria_label="Delete item",
    on_click=ctx.callback(handler),
)
```

---

## 5. Input Components

### `Input`

**Signature:**
```python
rc.Input(name: str | None = None, label: str | None = None, description: str | None = None, type: Literal['text', 'email', 'password', 'number', 'tel', 'url', 'search'] = 'text', placeholder: str = '', value: str | None = None, default_value: str | None = None, required: bool = False, disabled: bool = False, read_only: bool = False, error: str | None = None, debounce: int = 0, on_change: Any = None, on_blur: Any = None, on_focus: Any = None, on_keydown: Any = None, on_keyup: Any = None, on_input: Any = None, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)
```
```python
rc.Input(
    name="email",
    label="Email Address",
    description="We'll never share your email.",
    type="email",            # "text"|"email"|"password"|"number"|"tel"|"url"|"search"
    placeholder="you@example.com",
    value=None,              # controlled value (None = uncontrolled)
    default_value=None,
    required=True,
    disabled=False,
    read_only=False,
    error="Invalid email",   # shown below input
    debounce=300,            # ms delay before on_change fires
    on_change=ctx.callback(handler),
    on_blur=ctx.callback(handler),
    on_focus=ctx.callback(handler),
    on_keydown=ctx.callback(handler),
)
```

### `Textarea`

**Signature:**
```python
rc.Textarea(name: str | None = None, label: str | None = None, description: str | None = None, placeholder: str = '', value: str | None = None, default_value: str | None = None, rows: int = 3, required: bool = False, disabled: bool = False, error: str | None = None, debounce: int = 0, on_change: Any = None, on_blur: Any = None, on_focus: Any = None, on_keydown: Any = None, on_keyup: Any = None, on_input: Any = None, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)
```
```python
rc.Textarea(
    name="bio",
    label="Biography",
    placeholder="Tell us about yourself…",
    rows=5,
    debounce=300,
    on_change=ctx.callback(handler),
)
```

### `Select`

**Signature:**
```python
rc.Select(options: list[dict[str, str]], name: str | None = None, label: str | None = None, description: str | None = None, value: str | None = None, default_value: str | None = None, placeholder: str = 'Select...', required: bool = False, disabled: bool = False, error: str | None = None, on_change: Any = None, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)
```
```python
rc.Select(
    name="country",
    label="Country",
    options=[
        {"value": "us", "label": "United States"},
        {"value": "de", "label": "Germany", "disabled": True},
    ],
    value=None,              # controlled
    placeholder="Choose…",
    required=True,
    error=None,
    on_change=ctx.callback(handler),
)
```

### `Checkbox`

**Signature:**
```python
rc.Checkbox(name: str | None = None, value: str | None = None, label: str | None = None, description: str | None = None, checked: bool = False, default_checked: bool = False, required: bool = False, disabled: bool = False, error: str | None = None, on_change: Any = None, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)
```
```python
rc.Checkbox(
    name="agree",
    value="yes",
    label="I agree to the terms",
    checked=False,
    required=False,
    on_change=ctx.callback(handler),
)
```

### `CheckboxGroup`

**Signature:**
```python
rc.CheckboxGroup(name: str | None = None, children: ChildrenType = None, label: str | None = None, description: str | None = None, value: list[str] | None = None, default_value: list[str] | None = None, orientation: Literal['vertical', 'horizontal'] = 'vertical', required: bool = False, disabled: bool = False, error: str | None = None, on_change: Any = None, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)
```
```python
rc.CheckboxGroup(
    name="fruits",
    label="Favourite fruits",
    value=["apple"],         # controlled list
    orientation="vertical",  # "vertical"|"horizontal"
    error=None,
    on_change=ctx.callback(handler),  # ctx.event_data = {"value": ["apple", ...]}
    children=[
        rc.Checkbox(value="apple", label="Apple"),
        rc.Checkbox(value="banana", label="Banana"),
        rc.Checkbox(value="orange", label="Orange", disabled=True),
    ],
)
```

### `RadioGroup` / `Radio`

**Signatures:**
```python
rc.RadioGroup(name: str | None = None, children: ChildrenType = None, label: str | None = None, description: str | None = None, value: str | None = None, default_value: str | None = None, orientation: Literal['vertical', 'horizontal'] = 'vertical', required: bool = False, disabled: bool = False, error: str | None = None, on_change: Any = None, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)

rc.Radio(value: str, label: str | None = None, description: str | None = None, required: bool = False, disabled: bool = False, error: str | None = None, children: ChildrenType = None, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)
```
```python
rc.RadioGroup(
    name="plan",
    label="Select a plan",
    value="pro",             # controlled
    orientation="vertical",
    on_change=ctx.callback(handler),  # ctx.event_data = {"value": "pro"}
    children=[
        rc.Radio(value="free", label="Free"),
        rc.Radio(value="pro", label="Pro"),
    ],
)
```

---

## 6. Form Components

### `Form`

**Signature:**
```python
rc.Form(children: ChildrenType = None, on_submit: Any = None, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)
```
Intercepts submit, routes to server via WebSocket:
```python
rc.Form(
    on_submit=ctx.callback(handle_submit),  # ctx.event_data = form field dict
    children=[
        rc.Input(name="email", label="Email", type="email"),
        rc.Input(name="password", label="Password", type="password"),
        rc.Button("Submit", type="submit"),
    ],
)
```

### `FormField`

**Signature:**
```python
rc.FormField(children: ChildrenType = None, label: str | None = None, error: str | None = None, hint: str | None = None, required: bool = False, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)
```
```python
rc.FormField(
    label="Password",
    hint="At least 8 characters.",
    required=True,
    error="Too short.",
    children=[rc.Input(name="password", type="password")],
)
```

### `Label`

**Signature:**
```python
rc.Label(text: str, html_for: str | None = None, required: bool = False, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)
```
```python
rc.Label(text="API Key", html_for="api-key-input", required=True)
```

### `InputWrapper`

**Signature:**
```python
rc.InputWrapper(label: str | None = None, description: str | None = None, required: bool = False, error: str | None = None, children: ChildrenType = None, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)
```
Wraps any custom control with label/description/error chrome:
```python
rc.InputWrapper(
    label="Volume",
    description="Adjust playback volume.",
    required=True,
    error=None,
    children=[rc.Slider(value=[75], min=0, max=100)],
)
```

---

## 7. Advanced Controls

### `Switch`

**Signature:**
```python
rc.Switch(checked: bool | None = None, default_checked: bool = False, disabled: bool = False, name: str | None = None, on_checked_change: Any = None, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)
```
```python
rc.Switch(
    checked=True,
    disabled=False,
    name="notifications",
    on_checked_change=ctx.callback(handler),  # ctx.event_data = True/False
)
```

### `Slider`

**Signature:**
```python
rc.Slider(value: list[float] | None = None, default_value: list[float] | None = None, min: float = 0, max: float = 100, step: float = 1, disabled: bool = False, orientation: Literal['horizontal', 'vertical'] = 'horizontal', label: str | None = None, description: str | None = None, show_value: bool = False, required: bool = False, error: str | None = None, on_value_change: Any = None, on_value_commit: Any = None, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)
```
```python
rc.Slider(
    label="Volume",
    value=[50],              # list[float]; two values = range slider
    min=0, max=100, step=1,
    show_value=True,
    orientation="horizontal",
    on_value_change=ctx.callback(handler),  # ctx.event_data = [50]
    on_value_commit=ctx.callback(handler),  # fires when user releases
)
```

### `Toggle` / `ToggleGroup`

**Signatures:**
```python
rc.Toggle(label: str = '', icon: str | None = None, pressed: bool | None = None, default_pressed: bool = False, disabled: bool = False, variant: Literal['default', 'outline'] = 'default', size: Literal['sm', 'md', 'lg'] = 'md', on_pressed_change: Any = None, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)

rc.ToggleGroup(type: Literal['single', 'multiple'] = 'single', value: str | list[str] | dict[str, bool] | None = None, default_value: str | list[str] | dict[str, bool] | None = None, disabled: bool = False, variant: Literal['default', 'outline'] = 'default', size: Literal['sm', 'md', 'lg'] = 'md', on_value_change: Any = None, children: ChildrenType = None, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)

rc.ToggleGroupItem(label: str = '', icon: str | None = None, value: str | None = None, name: str | None = None, disabled: bool = False, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)
```
```python
rc.Toggle(
    label="Bold",
    icon="Bold",
    pressed=True,
    on_pressed_change=ctx.callback(handler),
)

rc.ToggleGroup(
    type="multiple",         # "single"|"multiple"
    default_value={"bold": True, "italic": False},
    on_value_change=ctx.callback(handler),
    children=[
        rc.ToggleGroupItem("Bold", icon="Bold", name="bold"),
        rc.ToggleGroupItem("Italic", icon="Italic", name="italic"),
    ],
)
```

### `Calendar` / `DatePicker`

**Signatures:**
```python
rc.Calendar(mode: Literal['single', 'multiple', 'range'] = 'single', caption_layout: Literal['label', 'dropdown', 'dropdown-months', 'dropdown-years'] = 'label', selected: Any = None, default_month: Any = None, disabled: bool = False, show_outside_days: bool = True, show_week_number: bool = False, min_date: Any = None, max_date: Any = None, number_of_months: int | None = None, on_select: Any = None, on_month_change: Any = None, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)

rc.DatePicker(value: Any = None, placeholder: str = 'Pick a date', disabled: bool = False, format: str = 'PPP', mode: Literal['single', 'multiple', 'range'] = 'single', caption_layout: Literal['label', 'dropdown', 'dropdown-months', 'dropdown-years'] = 'label', min_date: Any = None, max_date: Any = None, number_of_months: int | None = None, label: str | None = None, description: str | None = None, required: bool = False, error: str | None = None, on_change: Any = None, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)
```
```python
from datetime import date
rc.Calendar(
    mode="single",           # "single"|"multiple"|"range"
    selected=date(2026, 5, 31),
    on_select=ctx.callback(handler),
)

rc.DatePicker(
    value="2026-05-31",      # ISO date string
    placeholder="Pick a date",
    on_change=ctx.callback(handler),
)
```

### `Combobox`

**Signature:**
```python
rc.Combobox(options: list[ComboboxOption] | None = None, value: str | list[str] | None = None, placeholder: str = 'Select...', search_placeholder: str = 'Search...', empty_text: str = 'No results found.', multiselect: bool = False, disabled: bool = False, label: str | None = None, description: str | None = None, required: bool = False, error: str | None = None, on_select: Any = None, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)
```
```python
rc.Combobox(
    options=[{"value": "react", "label": "React"}, ...],
    value="react",
    placeholder="Select framework…",
    search_placeholder="Search…",
    on_change=ctx.callback(handler),
)
```

---

## 8. Card Components

**Signatures:**
```python
rc.Card(children: ChildrenType = None, title: str | None = None, description: str | None = None, on_click: Any = None, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)

rc.CardHeader(title: str | None = None, description: str | None = None, children: ChildrenType = None, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)

rc.CardContent(children: ChildrenType = None, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)

rc.CardFooter(children: ChildrenType = None, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)

rc.CardTitle(children: ChildrenType = None, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)

rc.CardDescription(children: ChildrenType = None, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)
```

```python
# Full composition:
rc.Card(
    id="my-card",
    on_click=ctx.callback(handler),   # makes card interactive
    children=[
        rc.CardHeader(
            title="Dashboard",
            description="Overview",
        ),
        rc.CardContent(children=[rc.Text("Main content")]),
        rc.CardFooter(children=[
            rc.Button("Cancel", variant="outline"),
            rc.Button("Save", on_click=ctx.callback(save)),
        ]),
    ]
)

# Shorthand:
rc.Card(title="Quick Card", description="Subtitle", children=[...])
```

Sub-components: `CardTitle`, `CardDescription`, `CardHeader`, `CardContent`, `CardFooter`.

---

## 9. Data Display Components

### `Table` (low-level, full control)

**Signatures:**
```python
rc.Table(children: ChildrenType = None, id: str | None = None, class_name: str = '', striped: bool = False, hoverable: bool = True, style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)

rc.TableHeader(children: ChildrenType = None, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)

rc.TableRow(children: ChildrenType = None, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)

rc.TableHead(children: ChildrenType = None, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)

rc.TableBody(children: ChildrenType = None, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)

rc.TableCell(children: ChildrenType = None, col_span: int | None = None, row_span: int | None = None, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)
```
```python
rc.Table(
    hoverable=True,
    children=[
        rc.TableHeader(children=[
            rc.TableRow(children=[
                rc.TableHead(children=["Name"]),
                rc.TableHead(children=["Email"], class_name="text-right"),
            ])
        ]),
        rc.TableBody(children=[
            rc.TableRow(children=[
                rc.TableCell(children=["Alice"]),
                rc.TableCell(children=["alice@example.com"], class_name="text-right"),
            ]),
        ]),
    ]
)
```

### `DataTable` (batteries included — sorting, filtering, pagination)

**Signature:**
```python
rc.DataTable(columns: list[dict[str, Any]], data: list[dict[str, Any]], sortable: bool = True, filterable: bool = True, paginated: bool = True, page_size: int = 10, loading: bool = False, empty_message: str = 'No data available', current_page: int | None = None, on_row_click: Any = None, on_sort_change: Any = None, on_filter_change: Any = None, on_page_change: Any = None, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)
```
```python
rc.DataTable(
    columns=[
        {"key": "id",    "header": "#",     "width": "60px", "align": "right"},
        {"key": "name",  "header": "Name",  "sortable": True},
        {"key": "email", "header": "Email", "sortable": True},
        {"key": "role",  "header": "Role",  "align": "center"},
    ],
    data=[
        {"id": 1, "name": "Alice", "email": "alice@example.com", "role": "Admin"},
        {"id": 2, "name": "Bob",   "email": "bob@example.com",   "role": "Editor"},
    ],
    sortable=True,
    filterable=True,
    paginated=True,
    page_size=10,
    loading=False,
    empty_message="No records found.",
    on_row_click=ctx.callback(handler),       # ctx.event_data = row dict
    on_sort_change=ctx.callback(handler),     # ctx.event_data = {"key": "name", "direction": "asc"}
    on_filter_change=ctx.callback(handler),   # ctx.event_data = {"value": "alice"}
    on_page_change=ctx.callback(handler),     # ctx.event_data = {"page": 2}
)
# Column values can be Component instances (e.g. Badge); they are serialized automatically.
```

### `Badge`

**Signature:**
```python
rc.Badge(children: ChildrenType = None, variant: Literal['default', 'secondary', 'destructive', 'outline', 'success', 'warning'] = 'default', icon: str | None = None, icon_position: Literal['left', 'right'] = 'left', size: Literal['xs', 'sm', 'md', 'lg', 'xl'] = 'md', id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)
```
```python
rc.Badge("Active", variant="success")
rc.Badge(children=["New"], icon="star", icon_position="left", size="md")
# variants: "default"|"secondary"|"destructive"|"outline"|"success"|"warning"
# sizes: "xs"|"sm"|"md"|"lg"|"xl"
```

### `Avatar`

**Signature:**
```python
rc.Avatar(src: str | None = None, alt: str = '', fallback: str | None = None, size: Literal['sm', 'md', 'lg'] = 'md', id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)
```
```python
rc.Avatar(src="/avatars/alice.jpg", alt="Alice", size="lg")
rc.Avatar(fallback="JD", size="md")   # initials fallback
```

### `Tooltip`

**Signature:**
```python
rc.Tooltip(content: str, children: ChildrenType = None, side: Literal['top', 'right', 'bottom', 'left'] = 'top', side_offset: int | None = None, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)
```
```python
rc.Tooltip(
    content="This cannot be undone.",
    side="top",       # "top"|"right"|"bottom"|"left"
    children=[rc.Button("Delete", variant="destructive")],
)
```

### `Tabs` / `TabItem`

**Signatures:**
```python
rc.Tabs(children: ChildrenType = None, default_value: str | None = None, value: str | None = None, on_value_change: Any = None, direction: Literal['horizontal', 'vertical'] = 'horizontal', size: Literal['xs', 'sm', 'md', 'lg', 'xl'] = 'md', gap: int | None = None, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)

rc.TabItem(value: str, label: str = '', icon: str | None = None, children: ChildrenType = None, disabled: bool = False, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)
```
```python
rc.Tabs(
    default_value="overview",
    value=None,                      # controlled
    direction="horizontal",          # "horizontal"|"vertical"
    on_value_change=ctx.callback(handler),
    children=[
        rc.TabItem(value="overview", label="Overview", icon="home",
                   children=[rc.Text("Overview content")]),
        rc.TabItem(value="settings", label="Settings",
                   children=[rc.Text("Settings content")]),
        rc.TabItem(value="disabled", label="Disabled", disabled=True, children=[]),
    ],
)
```

### `Accordion`

**Signatures:**
```python
rc.Accordion(children: ChildrenType = None, type: Literal['single', 'multiple'] = 'single', collapsible: bool = True, default_value: str | list[str] | None = None, value: str | list[str] | None = None, on_value_change: Any = None, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)

rc.AccordionItem(value: str, children: ChildrenType = None, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)

rc.AccordionTrigger(children: ChildrenType = None, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)

rc.AccordionContent(children: ChildrenType = None, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)
```
```python
rc.Accordion(
    type="single",              # "single"|"multiple"
    collapsible=True,
    default_value="item-1",
    on_value_change=ctx.callback(handler),
    children=[
        rc.AccordionItem(value="item-1", children=[
            rc.AccordionTrigger(children=["Is it accessible?"]),
            rc.AccordionContent(children=[rc.Text("Yes.")]),
        ]),
        rc.AccordionItem(value="item-2", children=[
            rc.AccordionTrigger(children=["Is it styled?"]),
            rc.AccordionContent(children=[rc.Text("Yes.")]),
        ]),
    ],
)
```

### `List` / `ListItem`

**Signature:**
```python
rc.List(children: ChildrenType = None, ordered: bool = False, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)
```
```python
rc.List(children=["Apples", "Bananas", "Cherries"])
rc.List(ordered=True, children=["First step", "Second step"])
```

### `Image`

**Signature:**
```python
rc.Image(src: str, alt: str = '', width: int | str | None = None, height: int | str | None = None, object_fit: Literal['contain', 'cover', 'fill', 'none', 'scale-down'] = 'cover', loading: bool = False, fallback_src: str | None = None, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)
```
```python
rc.Image(src="/path/to/image.jpg", alt="Description", width=400, height=300)
```

---

## 10. Feedback Components

### `Alert`

**Signature:**
```python
rc.Alert(title: str | None = None, message: str | None = None, variant: Literal['default', 'success', 'warning', 'destructive', 'info'] = 'default', dismissible: bool = False, on_dismiss: Any = None, children: ChildrenType = None, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)
```
```python
rc.Alert(
    title="Heads up!",
    message="Something changed.",
    variant="default",   # "default"|"success"|"warning"|"destructive"|"info"
    dismissible=True,
    on_dismiss=ctx.callback(handler),
)
```

### `Progress`

**Signature:**
```python
rc.Progress(value: int = 0, max: int = 100, label: str | None = None, show_value: bool = False, foreground_color: Optional[Literal['primary', 'secondary', 'destructive', 'muted', 'accent', 'popover', 'card', 'background', 'foreground']] = None, track_color: str | None = None, striped: Optional[Literal['static', 'animated']] = None, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)
```
```python
rc.Progress(
    value=65,
    max=100,
    label="Uploading…",
    show_value=True,
    foreground_color="primary",
    striped="animated",          # None|"static"|"animated"
)
```

### `Spinner`

**Signature:**
```python
rc.Spinner(size: Literal['sm', 'md', 'lg'] = 'md', id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)
```
```python
rc.Spinner(size="md")   # "sm"|"md"|"lg"
```

### `Skeleton`

**Signature:**
```python
rc.Skeleton(width: str | int | None = None, height: str | int | None = None, variant: Literal['text', 'circular', 'rectangular'] = 'text', circle: bool = False, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)
```
```python
rc.Skeleton(width="100%", height="1rem", variant="text")
rc.Skeleton(width=40, height=40, circle=True)
```

### `ConnectionStatus`

**Signature:**
```python
rc.ConnectionStatus(children_connected: ChildrenType = None, children_disconnected: ChildrenType = None, position: Literal['top-left', 'top-right', 'bottom-left', 'bottom-right', 'inline'] = 'bottom-right', on_disconnect: Any = None, on_reconnect: Any = None, js_on_disconnect: Any = None, js_on_reconnect: Any = None, debounce_ms: int = 500, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)
```
```python
rc.ConnectionStatus(
    children_connected=[rc.Badge("Online", variant="success")],
    children_disconnected=[rc.Alert(title="Connection Lost", variant="destructive")],
    position="bottom-right",   # "top-left"|"top-right"|"bottom-left"|"bottom-right"|"inline"
    on_disconnect=ctx.callback(handler),
    on_reconnect=ctx.callback(handler),
    debounce_ms=500,
)
```

---

## 11. Overlay Components

### `Dialog`

**Signatures:**
```python
rc.Dialog(open: bool | None = None, default_open: bool = False, on_open_change: Any = None, title: str | None = None, description: str | None = None, confirm_label: str = 'Continue', cancel_label: str = 'Cancel', on_confirm: Any = None, on_cancel: Any = None, trigger: Any = None, variant: Literal['default', 'destructive'] = 'default', children: ChildrenType = None, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)

rc.DialogTrigger(children: ChildrenType = None, as_child: bool = False, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)

rc.DialogContent(children: ChildrenType = None, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)

rc.DialogHeader(children: ChildrenType = None, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)

rc.DialogTitle(title: str, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)

rc.DialogDescription(description: str, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)

rc.DialogFooter(children: ChildrenType = None, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)

rc.DialogAction(label: str, on_click: Any = None, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)

rc.DialogCancel(label: str = 'Cancel', on_click: Any = None, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)
```
```python
rc.Dialog(
    open=ctx.state.get("dialog_open", False),
    on_open_change=ctx.callback(on_open_change),
    children=[
        rc.DialogContent(children=[
            rc.DialogHeader(children=[
                rc.DialogTitle("Confirm Deletion"),
                rc.DialogDescription("This cannot be undone."),
            ]),
            rc.DialogFooter(children=[
                rc.Button("Cancel", variant="outline", on_click=ctx.callback(close_dialog)),
                rc.Button("Delete", variant="destructive", on_click=ctx.callback(confirm_delete)),
            ]),
        ]),
    ],
)
```

### `Sheet`

**Signatures:**
```python
rc.Sheet(open: bool | None = None, default_open: bool = False, on_open_change: Any = None, children: ChildrenType = None, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)

rc.SheetTrigger(children: ChildrenType = None, as_child: bool = False, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)

rc.SheetContent(children: ChildrenType = None, side: Literal['top', 'right', 'bottom', 'left'] = 'right', id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)

rc.SheetHeader(children: ChildrenType = None, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)

rc.SheetTitle(title: str, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)

rc.SheetDescription(description: str, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)

rc.SheetFooter(children: ChildrenType = None, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)

rc.SheetClose(children: ChildrenType = None, as_child: bool = False, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)
```
Slide-in panel from an edge:
```python
rc.Sheet(
    open=ctx.state.get("sheet_open", False),
    on_open_change=ctx.callback(handle_open),
    side="right",        # "top"|"right"|"bottom"|"left"
    children=[
        rc.SheetContent(children=[
            rc.SheetHeader(children=[rc.SheetTitle("Settings")]),
            rc.Container(children=[...form...]),
        ]),
    ],
)
```

### `Popover`

**Signatures:**
```python
rc.Popover(open: bool | None = None, default_open: bool = False, on_open_change: Any = None, trigger: Any = None, side: Literal['top', 'right', 'bottom', 'left'] = 'bottom', align: Literal['start', 'center', 'end'] = 'center', children: ChildrenType = None, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)

rc.PopoverTrigger(children: ChildrenType = None, as_child: bool = False, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)

rc.PopoverContent(children: ChildrenType = None, side: Literal['top', 'right', 'bottom', 'left'] = 'bottom', side_offset: int = 4, align: Literal['start', 'center', 'end'] = 'center', id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)
```
```python
rc.Popover(
    children=[
        rc.PopoverTrigger(children=[rc.Button("Open")]),
        rc.PopoverContent(children=[rc.Text("Popover content")]),
    ]
)
```

### `DropdownMenu`

**Signatures:**
```python
rc.DropdownMenu(open: bool | None = None, default_open: bool = False, on_open_change: Any = None, children: ChildrenType = None, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)

rc.DropdownMenuTrigger(children: ChildrenType = None, as_child: bool = False, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)

rc.DropdownMenuContent(children: ChildrenType = None, side: Literal['top', 'right', 'bottom', 'left'] = 'bottom', side_offset: int = 4, align: Literal['start', 'center', 'end'] = 'start', id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)

rc.DropdownMenuLabel(label: str, inset: bool = False, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)

rc.DropdownMenuSeparator(id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)

rc.DropdownMenuItem(label: str, icon: str | None = None, shortcut: str | None = None, disabled: bool = False, on_select: Any = None, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)

rc.DropdownMenuCheckboxItem(label: str, checked: bool = False, on_checked_change: Any = None, disabled: bool = False, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)

rc.DropdownMenuRadioGroup(value: str = '', on_value_change: Any = None, children: ChildrenType = None, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)

rc.DropdownMenuRadioItem(label: str, value: str = '', id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)

rc.DropdownMenuSub(children: ChildrenType = None, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)

rc.DropdownMenuSubTrigger(label: str, icon: str | None = None, inset: bool = False, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)

rc.DropdownMenuSubContent(children: ChildrenType = None, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)
```
```python
rc.DropdownMenu(children=[
    rc.DropdownMenuTrigger(children=[rc.Button("Options")]),
    rc.DropdownMenuContent(children=[
        rc.DropdownMenuLabel(label="Actions"),
        rc.DropdownMenuSeparator(),
        rc.DropdownMenuItem(label="Edit", icon="pencil", on_click=ctx.callback(handler)),
        rc.DropdownMenuItem(label="Delete", icon="trash", on_click=ctx.callback(handler)),
    ]),
])
```

---

## 12. Scroll Area

**Signatures:**
```python
rc.ScrollArea(children: ChildrenType = None, type: Literal['auto', 'always', 'scroll', 'hover'] = 'hover', scroll_hide_delay: int = 600, dir: Optional[Literal['ltr', 'rtl']] = None, stick_to_bottom: bool = False, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)

rc.ScrollBar(orientation: Literal['horizontal', 'vertical'] = 'vertical', id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)
```

```python
rc.ScrollArea(
    id="scroll-area",
    class_name="border rounded-lg p-4",
    style={"height": "500px"},
    stick_to_bottom=True,   # auto-scrolls to new content (for streaming/chat)
    children=[rc.Markdown(id="output", content="")],
)
```

`stick_to_bottom` auto-scrolls unless the user has scrolled up; re-sticks when they scroll back to the bottom.

---

## 13. Resizable Panels

**Signatures:**
```python
rc.ResizablePanelGroup(direction: Literal['horizontal', 'vertical'] = 'horizontal', children: ChildrenType = None, on_layout: Any = None, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)

rc.ResizablePanel(default_size: float = 50, min_size: float | None = None, max_size: float | None = None, collapsible: bool = False, collapsed_size: float | None = None, on_collapse: Any = None, on_expand: Any = None, on_resize: Any = None, children: ChildrenType = None, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)

rc.ResizableHandle(with_handle: bool = False, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)
```

```python
rc.ResizablePanelGroup(
    direction="horizontal",   # "horizontal"|"vertical"
    children=[
        rc.ResizablePanel(
            default_size=25, min_size=15, max_size=40,
            children=[rc.Text("Left panel")],
        ),
        rc.ResizableHandle(with_handle=True),
        rc.ResizablePanel(
            default_size=75,
            children=[rc.Text("Main content")],
        ),
    ],
)
```

---

## 14. Collapsible

**Signatures:**
```python
rc.Collapsible(open: bool | None = None, default_open: bool = False, on_open_change: Any = None, disabled: bool = False, children: ChildrenType = None, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)

rc.CollapsibleTrigger(children: ChildrenType = None, as_child: bool = True, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)

rc.CollapsibleContent(children: ChildrenType = None, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)
```

```python
rc.Collapsible(
    default_open=True,
    open=None,                # controlled
    on_open_change=ctx.callback(handler),
    children=[
        rc.CollapsibleTrigger(children=[rc.Button("Toggle Section")]),
        rc.CollapsibleContent(children=[rc.Text("Hidden content")]),
    ],
)
```

---

## 15. Utility & Interaction Components

### `Slot`
Placeholder component that can be replaced dynamically.
**Signature:**
```python
rc.Slot(children: ChildrenType = None, id: str | None = None, class_name: str = '', fallback: Component | None = None, extra_props: dict[str, Any] | None = None)
```

### `Kbd`
Keyboard key display.
**Signature:**
```python
rc.Kbd(key: str, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)
```

### `LoadingOverlay`
Global loading state overlay.
**Signature:**
```python
rc.LoadingOverlay(loading: bool = False, text: str = 'Loading...', blur: bool = True, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)
```

### `ThemeSwitcher`
Theme switcher component for toggling between light and dark themes.
**Signature:**
```python
rc.ThemeSwitcher(default_theme: Literal['light', 'dark', 'system'] = 'system', storage_key: str = 'refast-theme', show_system_option: bool = True, mode: Literal['toggle', 'dropdown'] = 'toggle', on_change: Any = None, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)
```

### `Timer`
An invisible component that repeatedly triggers a server callback at a
**Signature:**
```python
rc.Timer(interval: int = 1000, enabled: bool = True, on_tick: Any = None, id: str | None = None, extra_props: dict[str, Any] | None = None)
```

### `KeyboardShortcut`
An invisible component that captures keyboard shortcuts and triggers callbacks.
**Signature:**
```python
rc.KeyboardShortcut(shortcuts: dict[str, Any], priority: int = 0, bubble: bool = False, prevent_default: bool = True, enabled: bool = True, id: str | None = None, extra_props: dict[str, Any] | None = None)
```

### `Icon`
Icon component that renders Lucide icons by name.
**Signature:**
```python
rc.Icon(name: str, size: int = 16, color: str | None = None, stroke_width: float = 2, id: str | None = None, class_name: str = '', style: dict[str, Any] | None = None, parent_style: dict[str, Any] | None = None, extra_props: dict[str, Any] | None = None)
```

## Lazy-Loading Feature Bundles

Heavy components require their feature chunk to be loaded. Pass the chunk name(s) to `preloaded_features` on `RefastApp`:

```python
ui = RefastApp(
    title="My App",
    preloaded_features=["charts", "markdown", "icons"],
)
```

| Feature | Components |
|---------|-----------|
| `"charts"` | Chart components (ECharts extension etc.) |
| `"markdown"` | `Markdown` component |
| `"icons"` | Lucide icon rendering in all components |
| `"navigation"` | Sidebar, Menubar, NavigationMenu, Command |
| `"overlay"` | Dialog, Sheet, Popover, DropdownMenu |
| `"controls"` | Slider, Calendar, DatePicker, Combobox, InputOTP |

Omit `preloaded_features` to load everything (default). Pass `[]` for minimal bundle (core only).
