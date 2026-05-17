"""Styling — /docs/concepts/styling."""

from refast.components import Container, Heading, Markdown, Separator

PAGE_TITLE = "Styling"
PAGE_ROUTE = "/docs/concepts/styling"


def render(ctx):
    """Render the styling guide page."""
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
Refast uses **Tailwind CSS** for styling with a curated safelist to keep the
CSS bundle small (~1 MB). Components are styled via the `class_name` prop; truly
dynamic values use the `style` prop.

---

## The `class_name` Prop

Every component accepts a `class_name` string of Tailwind utility classes:

```python
Container(class_name="max-w-4xl mx-auto p-6 bg-card rounded-lg shadow")
Text("Hello", class_name="text-lg font-bold text-primary")
```

---

## ✅ Available Tailwind Classes

The following classes are explicitly safelisted in
`src/refast-client/tailwind.config.js` and are guaranteed to be present in the
compiled CSS bundle.

### Layout & Display

| Category | Classes |
|----------|---------|
| **Display** | `block`, `inline`, `flex`, `grid`, `table`, `hidden` — all support responsive variants `sm:`, `md:`, `lg:`, `xl:`, `2xl:` |
| **Position** | `absolute`, `relative`, `fixed`, `sticky` |
| **Inset reset** | `top-0`, `right-0`, `bottom-0`, `left-0`, `inset-0` *(only `-0` variant is safelisted)* |
| **Z-index** | `z-0`, `z-10`, `z-20`, `z-30`, `z-40`, `z-50` |
| **Overflow** | `overflow-auto`, `overflow-hidden`, `overflow-visible`, `overflow-scroll` |

### Sizing

| Category | Classes |
|----------|---------|
| **Width / Height** | `w-full`, `w-screen`, `w-auto`, `w-min`, `w-max`, `w-fit`; same for `h-` |
| **Max-width** | `max-w-{xs\|sm\|md\|lg\|xl\|2xl–7xl\|full\|min\|max\|fit\|prose}` |
| **Max-width screen** | `max-w-screen-{sm\|md\|lg\|xl\|2xl}` |

### Spacing

Spacing scale: **0–6, 8, 10, 12, 16, auto**.  
Supports `p`, `px`, `py`, `pt`, `pr`, `pb`, `pl` and the same for `m`.

```python
Container(class_name="p-4 mx-auto mt-6")
```

### Flexbox

| Class | Notes |
|-------|-------|
| `flex-row`, `flex-col`, `flex-row-reverse`, `flex-col-reverse` | Direction — responsive |
| `flex-wrap`, `flex-nowrap` | Wrapping — responsive |
| `flex-1`, `flex-auto`, `flex-none` | Growth shorthand — responsive |
| `grow`, `grow-0`, `shrink`, `shrink-0` | Explicit grow/shrink |
| `gap-{0–6,8}`, `gap-x-*`, `gap-y-*` | Gap — responsive |
| `justify-{start\|end\|center\|between\|around\|evenly\|stretch}` | Main axis |
| `items-{start\|end\|center\|stretch\|baseline}` | Cross axis |
| `self-{start\|end\|center\|stretch\|baseline}` | Individual self-alignment |
| `content-{start\|end\|center\|between\|around\|evenly\|stretch}` | Multi-line |

### Grid

| Class | Notes |
|-------|-------|
| `grid-cols-{1–6\|12\|none}` | Column count — responsive |
| `col-span-{1\|2\|3\|4\|6\|12\|full}` | Column span — responsive |
| `row-span-{1\|2\|3\|4\|6\|12\|full}` | Row span — responsive |

### Typography

| Category | Classes |
|----------|---------|
| **Size** | `text-xs`, `text-sm`, `text-base`, `text-lg`, `text-xl`, `text-2xl`, `text-3xl` |
| **Weight** | `font-normal`, `font-medium`, `font-semibold`, `font-bold` |
| **Align** | `text-left`, `text-center`, `text-right`, `text-justify` |
| **Whitespace** | `whitespace-nowrap`, `whitespace-pre`, `whitespace-normal` |
| **Space between** | `space-x-{0–6,8}`, `space-y-{0–6,8}` — responsive |

### Borders & Shadows

| Category | Classes |
|----------|---------|
| **Border width** | `border`, `border-0`, `border-2`, `border-4`, `border-8` |
| **Border sides** | `border-x`, `border-y`, `border-t`, `border-r`, `border-b`, `border-l` (+ `-0/-2/-4/-8`) |
| **Radius** | `rounded`, `rounded-{sm\|md\|lg\|xl\|2xl\|3xl\|full\|none}` |
| **Radius sides** | `rounded-t`, `rounded-r`, `rounded-b`, `rounded-l`, `rounded-{tl\|tr\|br\|bl}` |
| **Shadow** | `shadow`, `shadow-{sm\|md\|lg\|xl\|2xl\|inner\|none}` |

### Interaction & Animation

| Category | Classes |
|----------|---------|
| **Cursor** | `cursor-pointer`, `cursor-not-allowed`, `cursor-text`, `cursor-move` |
| **Outline** | `outline-none` |
| **Transition** | `transition`, `transition-colors`, `transition-opacity`, `transition-transform`, etc. |
| **Duration** | `duration-100`, `duration-200`, `duration-300`, `duration-500`, `duration-700`, `duration-1000` |

### Order

Only `order-first`, `order-last`, and `order-none` are safelisted.

---

## 🎨 Semantic Color Tokens

Use semantic tokens so components automatically adapt to light and dark mode.
**Never use raw color literals like `bg-blue-500` for brand colors** — use tokens.

Supported properties: `bg-`, `text-`, `border-` (with `hover:` variant) and `ring-`
(with `focus:` variant).

| Token | `bg-` | `text-` | `border-` | `ring-` |
|-------|:-----:|:-------:|:---------:|:-------:|
| `background` | ✅ | ✅ | ✅ | ✅ |
| `foreground` | ✅ | ✅ | ✅ | ✅ |
| `primary` / `primary-foreground` | ✅ | ✅ | ✅ | ✅ |
| `secondary` / `secondary-foreground` | ✅ | ✅ | ✅ | ✅ |
| `muted` / `muted-foreground` | ✅ | ✅ | ✅ | ✅ |
| `accent` / `accent-foreground` | ✅ | ✅ | ✅ | ✅ |
| `card` / `card-foreground` | ✅ | ✅ | ✅ | ✅ |
| `popover` / `popover-foreground` | ✅ | ✅ | ✅ | ✅ |
| `destructive` | ✅ | ✅ | ✅ | ✅ |
| `success` | ✅ | ✅ | ✅ | ✅ |
| `warning` | ✅ | ✅ | ✅ | ✅ |
| `info` | ✅ | ✅ | ✅ | ✅ |
| `input` | ✅ | ✅ | ✅ | ✅ |
| `border` | ✅ | ✅ | ✅ | ✅ |

```python
# Good — adapts to theme and dark mode
Div(class_name="bg-card text-card-foreground border rounded-lg p-6")
Button("Delete", class_name="bg-destructive text-foreground hover:bg-destructive")

# Bad — hard-coded, breaks dark mode
Div(class_name="bg-white text-black")
```

### Palette Colors

For data visualizations or badges where concrete colors are needed, a curated
palette is also safelisted with `hover:` variants:

| Palette | Shades |
|---------|--------|
| `red`, `orange`, `yellow`, `green`, `teal` | 50 · 100 · 200 · 300 · 400 · 500 · 600 · 700 · 800 · 900 · 950 |
| `blue`, `purple`, `pink`, `gray`, `slate` | (same shades) |

```python
Badge("New", class_name="bg-blue-500 text-white")
Badge("Error", class_name="bg-red-600 text-white hover:bg-red-700")
```

---

## ❌ Not Safelisted — Use the `style` Prop

The following common utilities are **not** included in the safelist to keep the
bundle small. Use the `style` prop for these:

| Unsupported class | `style` equivalent |
|-------------------|--------------------|
| `w-64`, `h-10`, `w-1/2`, `h-[300px]` | `style={"width": "16rem"}`, `style={"height": "2.5rem"}` |
| `top-4`, `left-1/2`, `right-8` | `style={"top": "1rem"}`, `style={"left": "50%"}` |
| `opacity-50`, `opacity-75` | `style={"opacity": 0.5}` |
| `text-4xl`, `text-5xl`, `text-6xl` | `style={"fontSize": "2.25rem"}` |
| `font-light`, `font-extrabold`, `font-black` | `style={"fontWeight": 300}` |
| `order-1`, `order-2`, … (numeric) | `style={"order": 2}` |
| `min-w-*`, `min-h-*` | `style={"minWidth": "...", "minHeight": "..."}` |
| `gap-10`, `gap-12` (beyond 8) | `style={"gap": "2.5rem"}` |

```python
# ✅ Correct
Div(
    class_name="bg-muted rounded-md overflow-hidden",
    style={"width": "100%", "height": "300px"},
)

# Tooltip positioned relative to parent
Div(
    class_name="absolute bg-popover border p-2 rounded shadow-md",
    style={"top": "50px", "right": "20px", "maxWidth": "200px"},
)

# ❌ Wrong — these classes are not in the bundle
Div(class_name="w-full h-[300px]")
Div(class_name="top-4 right-8")
```

> **Rule of thumb:** Use `class_name` for structural, spacing, and semantic
> styling. Use `style` for anything involving specific numeric dimensions,
> positions, or values computed at runtime.

---

## Responsive Design

All display, flex, grid, gap, space, and col/row-span classes support the
standard Tailwind breakpoint prefixes:

| Prefix | Min-width |
|--------|-----------|
| `sm:` | 640 px |
| `md:` | 768 px |
| `lg:` | 1024 px |
| `xl:` | 1280 px |
| `2xl:` | 1536 px |

```python
# 1 column on mobile, 3 on medium screens, 4 on large
Div(class_name="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-6")

# Full-width sidebar on mobile, fixed width via style on desktop
Div(
    class_name="flex-1 md:flex-none",
    style={"width": "16rem"},  # md breakpoint width handled by style
)
```

---

## Interactive States

`hover:` is supported for `bg-`, `text-`, and `border-` semantic tokens and
palette colors. `focus:` is supported for `ring-` tokens.

```python
Button(
    "Save",
    class_name=(
        "bg-primary text-primary-foreground "
        "hover:bg-primary/90 "          # opacity modifier on hover
        "transition-colors duration-200 "
        "cursor-pointer rounded-md px-4 py-2"
    ),
)

Input(class_name="border border-input focus:ring-2 focus:ring-primary rounded-md")
```

---

## The `style` Prop

Pass a dict of CSS property names (camelCase) to `style` for dynamic or
unsafelisted values:

```python
# Dynamic progress bar width
Container(
    class_name="bg-muted rounded-full overflow-hidden",
    style={"height": "8px"},
    children=[
        Div(
            class_name="bg-primary h-full transition-all duration-300",
            style={"width": f"{percent}%"},
        )
    ],
)
```

---

## Custom CSS

Inject arbitrary CSS into the page via `RefastApp`:

```python
from refast import RefastApp

ui = RefastApp(
    title="My App",
    custom_css=".my-spinner { animation: spin 1s linear infinite; }",
)

# Or as a stylesheet path served by FastAPI static files
ui = RefastApp(title="My App", custom_css="/static/styles.css")
```

---

## Common Patterns

### Themed Card

```python
Div(
    class_name="bg-card text-card-foreground border rounded-lg p-6 shadow-sm",
    children=[
        Text("Title", class_name="text-lg font-semibold"),
        Text("Subtitle", class_name="text-sm text-muted-foreground mt-1"),
    ],
)
```

### Responsive Dashboard Grid

```python
Div(
    class_name="grid grid-cols-1 md:grid-cols-3 gap-6 p-6",
    children=[stat_card(title, value) for title, value in metrics],
)
```

### Content Max-Width Wrapper

```python
Container(class_name="max-w-4xl mx-auto p-6")
```

---

## See Also

- [Theming](/docs/concepts/theming) — Theme tokens and dark mode
- [Building Components](/docs/advanced/component-dev) — Styling custom components
"""
