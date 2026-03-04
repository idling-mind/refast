"""Form Inputs — /docs/components/inputs."""

from refast.components import Container, Heading, Markdown, Separator


PAGE_TITLE = "Form Inputs"
PAGE_ROUTE = "/docs/components/inputs"


def render(ctx):
    """Render the form inputs reference page."""
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
## Overview

This section covers all text-input, selection, and form wrapper components:
single-line text inputs, multi-line textareas, native dropdowns, checkboxes,
radio buttons, searchable comboboxes, OTP inputs, date pickers, and form
container components.

---

## Input

A single-line text input with optional label, description, placeholder, validation, and event
callbacks.

```python
from refast.components.shadcn.input import Input

# Basic text input
Input(name="username", placeholder="Enter username")

# Email with label, description, validation, and debounce
Input(
    name="email",
    label="Email Address",
    description="We'll never share your email.",
    type="email",
    placeholder="you@example.com",
    required=True,
    error="Please enter a valid email",
    debounce=300,
    on_change=ctx.callback(handle_change),
)

# Read-only input
Input(name="user_id", value="usr-001", read_only=True)

# Password with all event hooks
Input(
    name="password",
    type="password",
    on_change=ctx.callback(handle_change),
    on_blur=ctx.callback(handle_blur),
    on_focus=ctx.callback(handle_focus),
    on_keydown=ctx.callback(handle_keydown),
)
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `name` | `str \| None` | `None` | HTML `name` attribute; omit to skip. |
| `label` | `str \| None` | `None` | Label text displayed above the input. |
| `description` | `str \| None` | `None` | Help text below the label. |
| `type` | `"text" \| "email" \| "password" \| "number" \| "tel" \| "url" \| "search"` | `"text"` | HTML input type. |
| `placeholder` | `str` | `""` | Placeholder text. |
| `value` | `str \| None` | `None` | Controlled value; `None` leaves the input uncontrolled. |
| `required` | `bool` | `False` | Shows a required asterisk. |
| `disabled` | `bool` | `False` | Disables interaction. |
| `read_only` | `bool` | `False` | Renders in read-only mode. |
| `error` | `str \| None` | `None` | Error message displayed below the input. |
| `debounce` | `int` | `0` | Milliseconds to delay `on_change` after the user stops typing. |
| `on_change` | `Callback \| None` | `None` | Fired when the value changes. |
| `on_blur` | `Callback \| None` | `None` | Fired when the input loses focus. |
| `on_focus` | `Callback \| None` | `None` | Fired when the input gains focus. |
| `on_keydown` | `Callback \| None` | `None` | Fired on key-down. |
| `on_keyup` | `Callback \| None` | `None` | Fired on key-up. |
| `on_input` | `Callback \| None` | `None` | Fired on every native input event. |
| `class_name` | `str` | `""` | Additional Tailwind classes. |

---

## Textarea

Multi-line text input, useful for longer free-text responses.

```python
from refast.components.shadcn.input import Textarea

Textarea(
    name="bio",
    label="Biography",
    description="Tell us a little about yourself.",
    placeholder="Write your bio here…",
    rows=5,
    required=True,
    debounce=300,
    on_change=ctx.callback(handle_change),
)
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `name` | `str \| None` | `None` | HTML `name` attribute; omit to skip. |
| `label` | `str \| None` | `None` | Label text. |
| `description` | `str \| None` | `None` | Help text. |
| `placeholder` | `str` | `""` | Placeholder text. |
| `value` | `str \| None` | `None` | Controlled value. |
| `rows` | `int` | `3` | Number of visible text rows. |
| `required` | `bool` | `False` | Shows a required asterisk. |
| `disabled` | `bool` | `False` | Disables interaction. |
| `error` | `str \| None` | `None` | Error message. |
| `debounce` | `int` | `0` | Milliseconds to delay `on_change`. |
| `on_change` | `Callback \| None` | `None` | Fired on value change. |
| `on_blur` | `Callback \| None` | `None` | Fired on blur. |
| `on_focus` | `Callback \| None` | `None` | Fired on focus. |
| `on_keydown` | `Callback \| None` | `None` | Fired on key-down. |
| `on_keyup` | `Callback \| None` | `None` | Fired on key-up. |
| `on_input` | `Callback \| None` | `None` | Fired on every input event. |
| `class_name` | `str` | `""` | Additional Tailwind classes. |

---

## Select

A native HTML `<select>` dropdown styled with shadcn conventions.

Options are plain dicts with `value` and `label` keys. Add `"disabled": True` to an option
to make it unselectable.

```python
from refast.components.shadcn.input import Select

Select(
    name="country",
    label="Country",
    options=[
        {"value": "us", "label": "United States"},
        {"value": "gb", "label": "United Kingdom"},
        {"value": "de", "label": "Germany", "disabled": True},
    ],
    placeholder="Choose a country…",
    required=True,
    on_change=ctx.callback(handle_change),
)
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `options` | `list[dict]` | *(required)* | List of `{"value": str, "label": str}` dicts. Add `"disabled": True` to disable an option. |
| `name` | `str \| None` | `None` | HTML `name` attribute. |
| `label` | `str \| None` | `None` | Label text. |
| `description` | `str \| None` | `None` | Help text. |
| `value` | `str \| None` | `None` | Controlled selected value. |
| `placeholder` | `str` | `"Select..."` | Placeholder option when nothing is selected. |
| `required` | `bool` | `False` | Shows a required asterisk. |
| `disabled` | `bool` | `False` | Disables the select. |
| `error` | `str \| None` | `None` | Error message. |
| `on_change` | `Callback \| None` | `None` | Fired when the selection changes. |
| `class_name` | `str` | `""` | Additional Tailwind classes. |

---

## Checkbox and CheckboxGroup

Use `Checkbox` for a single boolean toggle. Use `CheckboxGroup` to manage multiple related
checkboxes with shared state — the group's `on_change` callback receives a `list[str]` of
currently checked values.

```python
from refast.components.shadcn.input import Checkbox, CheckboxGroup

# Standalone checkbox
Checkbox(
    name="agree",
    value="yes",
    label="I agree to the terms of service",
    required=True,
    on_change=ctx.callback(handle_toggle),
)

# Group with pre-selected values
CheckboxGroup(
    name="fruits",
    label="Favorite fruits",
    description="Select all that apply.",
    value=["apple", "orange"],
    required=True,
    error="Please select at least one.",
    on_change=ctx.callback(handle_fruit_change),
    children=[
        Checkbox(value="apple",  label="Apple"),
        Checkbox(value="banana", label="Banana"),
        Checkbox(value="orange", label="Orange"),
        Checkbox(value="grape",  label="Grape", disabled=True),
    ],
)
```

### Checkbox props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `name` | `str \| None` | `None` | HTML `name` attribute. |
| `value` | `str \| None` | `None` | Value submitted when checked. |
| `label` | `str \| None` | `None` | Label text. |
| `description` | `str \| None` | `None` | Help text. |
| `checked` | `bool` | `False` | Controlled checked state. |
| `required` | `bool` | `False` | Shows a required asterisk. |
| `disabled` | `bool` | `False` | Disables interaction. |
| `error` | `str \| None` | `None` | Error message. |
| `on_change` | `Callback \| None` | `None` | Fired when checked state changes. Serialized as `on_checked_change`. |
| `class_name` | `str` | `""` | Additional Tailwind classes. |

### CheckboxGroup props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `name` | `str \| None` | `None` | Shared HTML `name` for form submission. |
| `label` | `str \| None` | `None` | Group label. |
| `description` | `str \| None` | `None` | Group help text. |
| `value` | `list[str]` | `[]` | Controlled list of checked values. |
| `orientation` | `"vertical" \| "horizontal"` | `"vertical"` | Layout direction. |
| `required` | `bool` | `False` | Shows a required asterisk. |
| `disabled` | `bool` | `False` | Disables all checkboxes. |
| `error` | `str \| None` | `None` | Group error message. |
| `on_change` | `Callback \| None` | `None` | Called with the updated `list[str]` on any change. |
| `children` | `list[Checkbox]` | `[]` | Individual `Checkbox` components. |
| `class_name` | `str` | `""` | Additional Tailwind classes. |

---

## Radio and RadioGroup

Use `Radio` for individual radio buttons. Use `RadioGroup` to manage a set of mutually
exclusive options; the `on_change` callback receives the newly selected value as a `str`.

```python
from refast.components.shadcn.input import Radio, RadioGroup

RadioGroup(
    name="plan",
    label="Subscription plan",
    description="Choose the plan that best fits your needs.",
    value="pro",
    required=True,
    on_change=ctx.callback(handle_plan_change),
    children=[
        Radio(value="free",       label="Free"),
        Radio(value="pro",        label="Pro"),
        Radio(value="enterprise", label="Enterprise", disabled=True),
    ],
)
```

### Radio props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `value` | `str` | *(required)* | The value emitted when this radio is selected. |
| `name` | `str \| None` | `None` | HTML `name` grouping attribute. |
| `label` | `str \| None` | `None` | Label text. |
| `description` | `str \| None` | `None` | Help text. |
| `checked` | `bool` | `False` | Controlled checked state. |
| `required` | `bool` | `False` | Shows a required asterisk. |
| `disabled` | `bool` | `False` | Disables this radio. |
| `error` | `str \| None` | `None` | Error message. |
| `on_change` | `Callback \| None` | `None` | Fired when this radio is selected. |
| `class_name` | `str` | `""` | Additional Tailwind classes. |

### RadioGroup props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `name` | `str \| None` | `None` | Shared HTML `name` attribute. |
| `label` | `str \| None` | `None` | Group label. |
| `description` | `str \| None` | `None` | Group help text. |
| `value` | `str \| None` | `None` | Controlled selected value. |
| `orientation` | `"vertical" \| "horizontal"` | `"vertical"` | Layout direction. |
| `required` | `bool` | `False` | Shows a required asterisk. |
| `disabled` | `bool` | `False` | Disables all radio buttons. |
| `error` | `str \| None` | `None` | Group error message. |
| `on_change` | `Callback \| None` | `None` | Called with the new `str` value. Serialized as `on_value_change`. |
| `children` | `list[Radio]` | `[]` | Individual `Radio` components. |
| `class_name` | `str` | `""` | Additional Tailwind classes. |

---

## InputWrapper

A low-level layout wrapper that applies consistent label, description, required indicator,
and error styling around any child component. The built-in inputs (`Input`, `Textarea`,
`Select`, etc.) wrap themselves automatically — use `InputWrapper` directly only when
building custom controls such as wrapping a `Slider` or third-party component.

```python
from refast.components.shadcn.input import InputWrapper
from refast.components.shadcn.controls import Slider

InputWrapper(
    label="Volume",
    description="Adjust the playback volume.",
    required=True,
    error="Volume must be set.",
    children=[
        Slider(value=[75], min=0, max=100),
    ],
)
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `label` | `str \| None` | `None` | Label text. |
| `description` | `str \| None` | `None` | Help text below the label. |
| `required` | `bool` | `False` | Shows a required asterisk. |
| `error` | `str \| None` | `None` | Error message below the control. |
| `children` | `ChildrenType` | `None` | The wrapped control(s). |
| `class_name` | `str` | `""` | Additional Tailwind classes. |

---

## Form, FormField, and Label

Use `Form` as a top-level form container. Use `FormField` to wrap individual inputs with a
label, hint text, and validation error. Use `Label` when you need a standalone label element.

```python
from refast.components.shadcn.form import Form, FormField, Label
from refast.components.shadcn.input import Input, Select
from refast.components.shadcn.button import Button

Form(
    on_submit=ctx.callback(handle_submit),
    children=[
        FormField(
            label="Full name",
            hint="As it appears on your ID.",
            required=True,
            children=[Input(name="full_name", placeholder="Jane Doe")],
        ),
        FormField(
            label="Role",
            error="Please select a role.",
            children=[
                Select(
                    name="role",
                    options=[
                        {"value": "admin",  "label": "Admin"},
                        {"value": "viewer", "label": "Viewer"},
                    ],
                ),
            ],
        ),
        Button("Submit", type="submit"),
    ],
)

# Standalone label
Label(text="API Key", html_for="api-key-input", required=True)
```

### Form props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `on_submit` | `Callback \| None` | `None` | Fired when the form is submitted. |
| `children` | `ChildrenType` | `None` | Form content. |
| `class_name` | `str` | `""` | Additional Tailwind classes. |

### FormField props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `label` | `str \| None` | `None` | Field label text. |
| `hint` | `str \| None` | `None` | Hint text displayed below the label. |
| `error` | `str \| None` | `None` | Validation error message. |
| `required` | `bool` | `False` | Shows a required asterisk. |
| `children` | `ChildrenType` | `None` | The wrapped input component(s). |
| `class_name` | `str` | `""` | Additional Tailwind classes. |

### Label props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `text` | `str` | *(required)* | Label text content. |
| `html_for` | `str \| None` | `None` | Associates the label with a control's `id`. |
| `required` | `bool` | `False` | Shows a required asterisk. |
| `class_name` | `str` | `""` | Additional Tailwind classes. |

---

## DatePicker and Calendar

`DatePicker` renders a trigger button that opens a calendar popover. `Calendar` renders an
inline calendar without a trigger. Both support `"single"`, `"multiple"`, and `"range"`
selection modes.

Date values can be Python `date`/`datetime` objects or ISO 8601 strings. Range mode expects
a `dict` with `"from"` and `"to"` keys.

```python
from refast.components.shadcn.controls import DatePicker, Calendar
from datetime import date

# Single date picker with label
DatePicker(
    label="Appointment date",
    description="Select the date of your appointment.",
    value=date(2026, 4, 15),
    placeholder="Pick a date",
    required=True,
    on_change=ctx.callback(handle_date_change),
)

# Date range picker with month/year dropdowns
DatePicker(
    label="Report period",
    mode="range",
    caption_layout="dropdown",
    placeholder="Select date range",
    min_date=date(2024, 1, 1),
    max_date=date(2026, 12, 31),
    on_change=ctx.callback(handle_range_change),
)

# Inline calendar
Calendar(
    mode="single",
    selected=date(2026, 3, 4),
    on_select=ctx.callback(handle_select),
)
```

### DatePicker props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `value` | `date \| list[date] \| dict \| str \| None` | `None` | Selected date(s). |
| `placeholder` | `str` | `"Pick a date"` | Button text when no date is selected. |
| `disabled` | `bool` | `False` | Disables the picker. |
| `format` | `str` | `"PPP"` | `date-fns` format string for the button label. |
| `mode` | `"single" \| "multiple" \| "range"` | `"single"` | Selection mode. |
| `caption_layout` | `"label" \| "dropdown" \| "dropdown-months" \| "dropdown-years"` | `"label"` | Calendar header navigation style. |
| `min_date` | `date \| str \| None` | `None` | Earliest selectable date. |
| `max_date` | `date \| str \| None` | `None` | Latest selectable date. |
| `number_of_months` | `int \| None` | `None` | Number of calendar months shown simultaneously. |
| `label` | `str \| None` | `None` | Label text above the picker. |
| `description` | `str \| None` | `None` | Help text below the label. |
| `required` | `bool` | `False` | Shows a required asterisk. |
| `error` | `str \| None` | `None` | Error message. |
| `on_change` | `Callback \| None` | `None` | Fired when the selection changes. |
| `class_name` | `str` | `""` | Additional Tailwind classes. |

### Calendar props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `mode` | `"single" \| "multiple" \| "range"` | `"single"` | Selection mode. |
| `selected` | `date \| list[date] \| dict \| None` | `None` | Controlled selected date(s). |
| `default_month` | `date \| None` | `None` | Initial month to display. |
| `caption_layout` | `"label" \| "dropdown" \| "dropdown-months" \| "dropdown-years"` | `"label"` | Header navigation style. |
| `disabled` | `bool` | `False` | Disables all interaction. |
| `show_outside_days` | `bool` | `True` | Show days from adjacent months. |
| `min_date` | `date \| str \| None` | `None` | Earliest selectable date. |
| `max_date` | `date \| str \| None` | `None` | Latest selectable date. |
| `number_of_months` | `int \| None` | `None` | Number of months displayed. |
| `on_select` | `Callback \| None` | `None` | Fired when the selection changes. |
| `on_month_change` | `Callback \| None` | `None` | Fired when the displayed month changes. |
| `class_name` | `str` | `""` | Additional Tailwind classes. |

---

## Combobox

A searchable select with type-ahead filtering. Supports single and multi-select modes.

```python
from refast.components.shadcn.controls import Combobox

# Single-select
Combobox(
    label="Framework",
    description="Select your primary framework.",
    options=[
        {"value": "next",   "label": "Next.js"},
        {"value": "react",  "label": "React"},
        {"value": "vue",    "label": "Vue"},
        {"value": "svelte", "label": "Svelte"},
    ],
    placeholder="Select framework…",
    search_placeholder="Search frameworks…",
    empty_text="No frameworks found.",
    required=True,
    on_select=ctx.callback(handle_select),
)

# Multi-select
Combobox(
    label="Tags",
    options=[
        {"value": "python", "label": "Python"},
        {"value": "ts",     "label": "TypeScript"},
    ],
    multiselect=True,
    value=["python"],
    on_select=ctx.callback(handle_tags),
)
```

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `options` | `list[dict]` | `[]` | List of `{"value": str, "label": str}` dicts. |
| `value` | `str \| list[str] \| None` | `None` | Controlled selected value(s). |
| `placeholder` | `str` | `"Select..."` | Trigger button text when nothing is selected. |
| `search_placeholder` | `str` | `"Search..."` | Placeholder inside the search input. |
| `empty_text` | `str` | `"No results found."` | Text shown when no options match the search. |
| `multiselect` | `bool` | `False` | Allow selecting multiple values. |
| `disabled` | `bool` | `False` | Disables the combobox. |
| `label` | `str \| None` | `None` | Label text. |
| `description` | `str \| None` | `None` | Help text. |
| `required` | `bool` | `False` | Shows a required asterisk. |
| `error` | `str \| None` | `None` | Error message. |
| `on_select` | `Callback \| None` | `None` | Fired when the selection changes. |
| `class_name` | `str` | `""` | Additional Tailwind classes. |

---

## InputOTP, InputOTPGroup, InputOTPSlot, InputOTPSeparator

A one-time password input composed from slot primitives. The simplest approach uses
`InputOTP` with `max_length` and lets the component auto-generate its layout. For custom
layouts compose `InputOTPGroup`, `InputOTPSlot`, and `InputOTPSeparator` as children.

```python
from refast.components.shadcn.controls import (
    InputOTP,
    InputOTPGroup,
    InputOTPSlot,
    InputOTPSeparator,
)

# Simple 6-digit OTP (auto-layout)
InputOTP(
    label="Verification Code",
    description="Enter the 6-digit code sent to your email.",
    max_length=6,
    required=True,
    on_complete=ctx.callback(handle_complete),
)

# Custom layout: two groups of 3 separated by a dash
InputOTP(
    max_length=6,
    on_complete=ctx.callback(handle_complete),
    children=[
        InputOTPGroup(children=[
            InputOTPSlot(index=0),
            InputOTPSlot(index=1),
            InputOTPSlot(index=2),
        ]),
        InputOTPSeparator(),
        InputOTPGroup(children=[
            InputOTPSlot(index=3),
            InputOTPSlot(index=4),
            InputOTPSlot(index=5),
        ]),
    ],
)
```

### InputOTP props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `max_length` | `int` | `6` | Total number of OTP characters. |
| `value` | `str \| None` | `None` | Controlled OTP value. |
| `disabled` | `bool` | `False` | Disables the input. |
| `pattern` | `str \| None` | `None` | Regex pattern to validate each character. |
| `label` | `str \| None` | `None` | Label text. |
| `description` | `str \| None` | `None` | Help text. |
| `required` | `bool` | `False` | Shows a required asterisk. |
| `error` | `str \| None` | `None` | Error message. |
| `on_change` | `Callback \| None` | `None` | Fired on every character change. |
| `on_complete` | `Callback \| None` | `None` | Fired when all slots are filled. |
| `children` | `ChildrenType` | `None` | Custom layout using `InputOTPGroup` / `InputOTPSlot` / `InputOTPSeparator`. |
| `class_name` | `str` | `""` | Additional Tailwind classes. |

### InputOTPGroup props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `children` | `list[InputOTPSlot]` | `[]` | `InputOTPSlot` components in this group. |
| `class_name` | `str` | `""` | Additional Tailwind classes. |

### InputOTPSlot props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `index` | `int` | `0` | Zero-based slot index within the parent `InputOTP`. |
| `class_name` | `str` | `""` | Additional Tailwind classes. |

### InputOTPSeparator props

`InputOTPSeparator` accepts no props besides `class_name`. It renders a visual `—`
separator between slot groups.
"""
