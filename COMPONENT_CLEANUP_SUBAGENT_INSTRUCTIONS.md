# Component Cleanup Subagent Instructions

## Objective
Standardize, clean up, and document all components across the Refast Python backend (`src/refast/components/`) and React frontend (`src/refast-client/src/components/`). Ensure identical structures, consistent props (e.g., `variant`, `size`), and thorough documentation.

## Core Principles
1. **No Backward Compatibility Required**: Prioritize clean, legible, and maintainable code over preserving old APIs.
2. **Alignment**: Python kwargs and React props must match exactly (with `snake_case` in Python corresponding to `camelCase` in React).
3. **Consistency**: Options like `variant`, `size`, `color`, etc., must be identical across all applicable components. Use Literal types in Python to enforce these.
4. **Grouped Documentation**: Components that go together (e.g., Sidebar and its subcomponents, ToggleGroups and Toggles, CheckboxGroups and Checkboxes) MUST be documented together in the same chapter/file.
5. **Testing**: Cleanup any tests that break due to API changes.

## Step-by-Step Task Execution

For each component group assigned to you:

### 1. Python Implementation (`src/refast/components/shadcn/`)
- Review the component class.
- Standardize the `__init__` arguments.
  - Require specific types (e.g., `Literal["default", "destructive", "outline"]`).
  - Set sensible defaults.
- Add comprehensive docstrings for the class and its arguments.
- Ensure the `render` method correctly serializes the props.
- Remove unnecessary wrapper code or dead code.

### 2. React Implementation (`src/refast-client/src/components/shadcn/`)
- Review the React component interface.
- Ensure the interface strictly matches the Python output (handling camelCase conversion naturally).
- Standardize Tailwind classes relying on the defined variants/sizes using `cva` or similar patterns if present.
- Strip out unused or bloated code.

### 3. Documentation (`docs_site/pages/components/`)
- Find the corresponding documentation file or create it.
- Document the entire set of related components together.
- Include Python code examples and rendered live demos.
- Explicitly list the available props, variants, and sizes.

### 4. Tests (`tests/`)
- Locate tests for the assigned components (e.g., `tests/unit/test_components.py`).
- Fix any broken tests resulting from prop standardizations.
- Remove tests for deprecated/removed features.

## Output
When reporting back, summarize:
1. Components modified (Python & React).
2. Props standardized (variants, sizes, etc.).
3. Documentation file updated.
4. Test files fixed.

---

## Section 5: Prop Alignment Audit

Ensure every explicitly-declared Python kwarg has a matching explicit TypeScript prop, and every
TypeScript prop that is populated from Python has a matching named Python kwarg. `**props` and
`...props` are kept but only as passthrough escape hatches — no component-specific prop may hide
inside them.

---

### The Alignment Contract

> **Rule**: Every **named** kwarg in a Python component's `__init__` — excluding the base-class
> set (`id`, `class_name`, `style`, `parent_style`, `**props`) — must have an **explicitly
> declared** prop in the TypeScript interface under its camelCase equivalent name.
>
> Conversely, every explicitly declared TypeScript prop that the Python `render()` sends must be
> a named kwarg in Python — not just something that falls through `_serialize_extra_props()`.

The `ComponentRenderer.tsx` pipeline calls `snakeToCamel()` on **all** keys in the props dict, so
Python always sends `snake_case` and TypeScript always receives `camelCase`. This conversion is
automatic and should never be worked around.

---

### snake_case → camelCase Mapping Reference

| Python (`snake_case`) | TypeScript (`camelCase`) |
|---|---|
| `class_name` | `className` |
| `on_click` | `onClick` |
| `on_change` | `onChange` |
| `on_submit` | `onSubmit` |
| `on_value_change` | `onValueChange` |
| `on_value_commit` | `onValueCommit` |
| `on_open_change` | `onOpenChange` |
| `on_checked_change` | `onCheckedChange` |
| `on_pressed_change` | `onPressedChange` |
| `on_dismiss` | `onDismiss` |
| `icon_position` | `iconPosition` |
| `default_value` | `defaultValue` |
| `default_checked` | `defaultChecked` |
| `default_open` | `defaultOpen` |
| `default_pressed` | `defaultPressed` |
| `aria_label` | `ariaLabel` |
| `stroke_width` | `strokeWidth` |
| `confirm_label` | `confirmLabel` |
| `cancel_label` | `cancelLabel` |
| `read_only` | `readOnly` |
| `min_length` | `minLength` |
| `max_length` | `maxLength` |
| `placeholder` | `placeholder` *(same)* |
| `disabled` | `disabled` *(same)* |
| `required` | `required` *(same)* |
| `type` | `type` *(same)* |

The pattern is always: split on `_`, capitalise every word after the first, rejoin with no separator.

---

### Step-by-Step Workflow

Apply this process to **every** Python / TypeScript file pair in the inventory below.

**Step A — Build the Python prop list**

List every named kwarg in `__init__`, skipping the base set (`id`, `class_name`, `style`,
`parent_style`, `**props`). Convert each to camelCase.

```text
Python kwarg        → camelCase
on_value_change     → onValueChange
default_value       → defaultValue
icon_position       → iconPosition
```

**Step B — Build the TypeScript prop list**

List every explicitly declared prop in the TypeScript `interface` or `type` for the component
(including props inherited from `BaseProps`, `React.HTMLAttributes`, etc.). Convert each to
snake_case.

```text
TypeScript prop     → snake_case
onValueChange       → on_value_change
defaultValue        → default_value
iconPosition        → icon_position
```

Note: props already covered by `React.ButtonHTMLAttributes` (`disabled`, `type`, `onClick`, etc.)
do **not** need to be re-declared in the interface, but they still count as "present on the TS
side" for this audit.

**Step C — Diff both lists**

- Props in Python but **not** in TypeScript → add them to the TypeScript interface explicitly.
- Props in TypeScript but **not** in Python → add them as named kwargs in Python `__init__` (or
  document a deliberate exception with a comment if the prop is intentionally browser-side only).

**Step D — Align Literal types and defaults**

For every shared prop verify:
- Allowed values match: the same union options appear in both `Literal[...]` and the TypeScript
  union type.
- Default values match.
- Nullability matches: `str | None` in Python ↔ `string | undefined` in TypeScript.

**Step E — Update `render()` to emit known props explicitly**

Every named kwarg must appear **by name** in the `props = { ... }` dict inside `render()`. Do not
rely on `_serialize_extra_props()` to transport a prop that has a named kwarg. Known props that
are `None` or falsy can be conditionally included, but they must not silently disappear via the
catch-all.

```python
# ✅ CORRECT — explicit
def render(self) -> dict[str, Any]:
    props: dict[str, Any] = {
        "variant": self.variant,
        "size": self.size,
        "disabled": self.disabled,
        "class_name": self.class_name,
        **self._serialize_extra_props(),   # only for genuinely open-ended HTML attrs
    }
    if self.on_click:
        props["on_click"] = self.on_click.serialize()
    return {"type": self.component_type, "id": self.id, "props": props, "children": [...]}

# ❌ WRONG — "size" hidden in extra_props
def render(self) -> dict[str, Any]:
    return {
        "type": self.component_type,
        "id": self.id,
        "props": {"variant": self.variant, **self._serialize_extra_props()},
        "children": [...],
    }
```

---

### Reference Example: Button (Gold Standard)

`src/refast/components/shadcn/button.py` + `src/refast-client/src/components/shadcn/button.tsx`
form the canonical aligned pair. Use them as a reference.

**Python `Button.__init__` named kwargs (step A):**

| Python kwarg | camelCase | Type |
|---|---|---|
| `label` | `label` | `str` — sent as a child string, not a prop |
| `variant` | `variant` | `Literal["default","secondary","destructive","outline","ghost","link"]` |
| `size` | `size` | `Literal["sm","md","lg","icon"]` |
| `icon` | `icon` | `str \| None` |
| `icon_position` | `iconPosition` | `Literal["left","right"]` |
| `disabled` | `disabled` | `bool` — covered by `ButtonHTMLAttributes` |
| `loading` | `loading` | `bool` |
| `type` *(stored as `button_type`)* | `type` | `Literal["button","submit","reset"]` — covered by `ButtonHTMLAttributes` |
| `on_click` | `onClick` | callback — covered by `ButtonHTMLAttributes` |

**TypeScript `ButtonProps` (step B):**

`ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement>` — so `disabled`, `type`,
`onClick` are inherited. Additionally declared explicitly: `variant`, `size`, `loading`, `icon`,
`iconPosition`.

**Diff (step C):** All Python kwargs have a matching TS prop. ✅

**Literal alignment (step D):** Both sides share the same six `variant` values and four `size`
values with the same defaults. ✅

**`render()` (step E):** Every kwarg except `label` (sent as a child) and `on_click` / `disabled`
/ `type` (conditionally included or native HTML) is explicitly in the props dict. ✅

---

### Anti-Patterns

**❌ Component-specific prop hidden in `**props` / `_serialize_extra_props()`**

```python
# BAD: "open" is a key prop but never named — floats through extra_props invisibly
class BadDialog(Component):
    def __init__(self, **props):
        super().__init__(**props)  # "open" buried here
```

```typescript
// BAD: TS has no idea "open" is coming — picked up by ...props at best
interface BadDialogProps { children?: React.ReactNode }
```

```python
# GOOD: named on both sides
class Dialog(Component):
    def __init__(self, open: bool | None = None, **props):
        super().__init__(**props)
        self.open = open

    def render(self):
        props: dict[str, Any] = {"class_name": self.class_name, **self._serialize_extra_props()}
        if self.open is not None:
            props["open"] = self.open
        ...
```

```typescript
// GOOD
interface DialogProps {
  open?: boolean;
  onOpenChange?: (open: boolean) => void;
  children?: React.ReactNode;
}
```

---

**❌ Mismatched Literal options**

```python
variant: Literal["default", "warning", "destructive"] = "default"  # "warning" added
```

```typescript
variant?: 'default' | 'destructive';  // "warning" silently ignored in TS
```

```typescript
// GOOD — identical union
variant?: 'default' | 'warning' | 'destructive';
```

---

**❌ Python kwarg set in `__init__` but never emitted in `render()`**

```python
def __init__(self, read_only: bool = False, **props):
    self.read_only = read_only  # stored but never sent!

def render(self):
    return {"props": {"class_name": self.class_name}}  # read_only missing
```

```python
# GOOD
def render(self):
    return {"props": {"read_only": self.read_only, "class_name": self.class_name}}
```

---

**❌ TypeScript prop defined but default differs from Python**

```python
size: Literal["sm", "md", "lg"] = "md"  # Python default = "md"
```

```typescript
size?: 'sm' | 'md' | 'lg' = 'sm'  // TS default = "sm" — mismatch!
```

---

### `**props` / `...props` Policy

`**props` (Python) and `...props` (TypeScript) are **intentionally kept**. They serve as escape
hatches for:

- HTML passthrough attributes (`data-*`, `aria-*`, `role`, etc.)
- Rarely-used native HTML attributes that are not worth top-level kwargs
- Context-specific attributes set by wrappers at call sites

> **The rule**: If a prop has a **specific, named purpose** in the component (variant, size,
> icon_position, on_click, loading, …), it **must be a named kwarg in Python** and a **named prop
> in the TypeScript interface**. It must never rely on catch-alls for transport. Only genuinely
> open-ended or HTML-passthrough attributes may legitimately travel through `**props`/`...props`.

---

### Python-Only Components (No TypeScript Counterpart)

Before treating a component as Python-only, perform these checks:

1. **Search for the component type string** in `src/refast-client/src/components/`:
   ```bash
   grep -r '"Form"' src/refast-client/src/components/
   ```
2. **Check `ComponentRenderer.tsx`** — search for the type name in the registry lookup.
3. **Check the component registry** (`src/refast-client/src/components/registry.ts`) for how
   components are registered.
4. **Check if it renders compositionally** inside another TypeScript component.

If no TypeScript counterpart exists after these checks:

- Create the TypeScript component interface and implementation in the appropriate `.tsx` file.
- Always include a `'data-refast-id'?: string` prop and apply it with `data-refast-id={dataRefastId}`.
- Register the new component in `src/refast-client/src/components/registry.ts`.
- Ensure the new TS component handles camelCase prop names (they arrive already converted).

---

### Component Inventory

Process each pair below. Tick off steps A–E when complete.

| Python file | TypeScript file | A | B | C | D | E |
|---|---|---|---|---|---|---|
| `shadcn/button.py` | `shadcn/button.tsx` | | | | | |
| `shadcn/card.py` | `shadcn/card.tsx` | | | | | |
| `shadcn/controls.py` | `shadcn/controls.tsx` | | | | | |
| `shadcn/data_display.py` | `shadcn/data_display.tsx` | | | | | |
| `shadcn/feedback.py` | `shadcn/feedback.tsx` | | | | | |
| `shadcn/form.py` | *investigate — no known TS counterpart* | | | | | |
| `shadcn/icon.py` | `shadcn/icon.tsx` | | | | | |
| `shadcn/input.py` | `shadcn/input.tsx` | | | | | |
| `shadcn/layout.py` | `shadcn/layout.tsx` | | | | | |
| `shadcn/navigation.py` | `shadcn/navigation.tsx` | | | | | |
| `shadcn/overlay.py` | `shadcn/overlay.tsx` | | | | | |
| `shadcn/typography.py` | `shadcn/typography.tsx` | | | | | |
| `shadcn/utility.py` | `shadcn/utility.tsx` | | | | | |

**Steps recap:**
- **A** — Python prop list built and mapped to camelCase
- **B** — TypeScript prop list built and mapped to snake_case
- **C** — Diff applied; both sides updated
- **D** — Literal types and defaults aligned
- **E** — `render()` emits all named props explicitly
