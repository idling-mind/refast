# Component Reference Section — Agent Instructions

## Section Goal

Provide a **complete API reference** for every UI component in Refast. Each page covers
a group of related components with props tables, code examples, and live rendered demos.

---

## Format for Each Component

For every component on a page, include:

1. **Heading** (h3) with the component name
2. **One-sentence description** of what it renders
3. **Code example** as a Markdown code block showing typical usage
4. **Props table** with columns: Prop | Type | Default | Description
5. **Live rendered example** using actual Refast components (not just code)
6. **Notes** about variants, sizes, or special behaviors

### Props Table Template

```markdown
| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `label` | `str` | (positional) | Button text |
| `variant` | `"default" \| "secondary"` | `"default"` | Visual variant |
```

### Live Example Pattern

After the code block, embed the actual component:

```python
# In render():
Column(gap=4, children=[
    Heading("Button", level=3),
    Markdown(text="...code and props table..."),
    # Live demo
    Card(class_name="p-4", children=[
        Row(gap=2, children=[
            Button("Default"),
            Button("Secondary", variant="secondary"),
            Button("Destructive", variant="destructive"),
            Button("Ghost", variant="ghost"),
        ]),
    ]),
])
```

---

## Pages

### 1. `layout.py` — Layout Components (`/docs/components/layout`)

**Read:** `src/refast/components/base.py`, `src/refast/components/shadcn/layout.py`

**Components to document:**
- `Container` — div wrapper (id, class_name, children, style)
- `Flex` — flexbox (direction, align, justify, gap, wrap)
- `Row` — Flex shortcut for direction="row"
- `Column` — Flex shortcut for direction="column"
- `Grid` — CSS grid (columns, gap)
- `Center` — Centers children
- `Box` — Generic container
- `Separator` — Horizontal/vertical divider (orientation)
- `AspectRatio` — Fixed aspect ratio container (ratio)
- `ScrollArea` / `ScrollBar` — Custom scrollable area
- `ResizablePanelGroup` / `ResizablePanel` / `ResizableHandle` — Split panes (direction, sizes)

---

### 2. `typography.py` — Typography (`/docs/components/typography`)

**Read:** `src/refast/components/shadcn/typography.py`

**Components to document:**
- `Heading` — h1-h6 (text, level)
- `Text` — inline span (text, class_name)
- `Paragraph` — block p (text)
- `Code` — inline code (text)
- `Link` — hyperlink (text, href, target)
- `Markdown` — rich text with GFM, syntax highlighting, KaTeX (text)
- `Label` — form label (text, html_for)
- `Badge` — status indicator (text, variant)
- `Kbd` — keyboard shortcut display (text)

---

### 3. `buttons.py` — Buttons & Actions (`/docs/components/buttons`)

**Read:** `src/refast/components/shadcn/button.py`, `src/refast/components/shadcn/controls.py`, `src/refast/components/shadcn/overlay.py`

**Components to document:**
- `Button` — variants (default, secondary, destructive, outline, ghost, link), sizes (default, sm, lg, icon), icon, disabled, on_click
- `IconButton` — icon-only button
- `Toggle` — pressed/unpressed toggle (pressed, on_pressed_change, variant)
- `ToggleGroup` / `ToggleGroupItem` — group of toggles (type single/multiple)
- `DropdownMenu` / `DropdownMenuTrigger` / `DropdownMenuContent` / `DropdownMenuItem` / `DropdownMenuLabel` / `DropdownMenuSeparator` / `DropdownMenuCheckboxItem` / `DropdownMenuRadioGroup` / `DropdownMenuRadioItem` / `DropdownMenuSub` / `DropdownMenuSubTrigger` / `DropdownMenuSubContent`
- `ContextMenu` / `ContextMenuTrigger` / `ContextMenuContent` / `ContextMenuItem` / `ContextMenuSeparator` / `ContextMenuCheckboxItem`

---

### 4. `inputs.py` — Form Inputs (`/docs/components/inputs`)

**Read:** `src/refast/components/shadcn/input.py`, `src/refast/components/shadcn/form.py`, `src/refast/components/shadcn/controls.py`

**Components to document:**
- `Input` — text input (placeholder, value, type, on_change, store_as, disabled)
- `InputWrapper` — input with label and description
- `Textarea` — multi-line (placeholder, value, rows, on_change, store_as)
- `Select` — dropdown (options, placeholder, value, on_value_change, store_as)
- `Checkbox` — single checkbox (label, checked, on_checked_change)
- `CheckboxGroup` — grouped checkboxes
- `Radio` / `RadioGroup` — radio selection (options, value, on_value_change)
- `Switch` — toggle switch (checked, on_checked_change, label)
- `Slider` — range slider (min, max, step, value, on_value_change)
- `DatePicker` — date selection
- `Combobox` — searchable select (options, placeholder, on_value_change)
- `InputOTP` / `InputOTPGroup` / `InputOTPSlot` / `InputOTPSeparator` — OTP input
- `Form` / `FormField` — form wrapper
- `Label` — form label

---

### 5. `cards.py` — Cards & Containers (`/docs/components/cards`)

**Read:** `src/refast/components/shadcn/card.py`, `src/refast/components/shadcn/utility.py`

**Components to document:**
- `Card` — bordered container
- `CardHeader` — card header section
- `CardTitle` — card title
- `CardDescription` — card subtitle
- `CardContent` — card body
- `CardFooter` — card footer
- `Collapsible` / `CollapsibleTrigger` / `CollapsibleContent` — expandable section

---

### 6. `data_display.py` — Data Display (`/docs/components/data-display`)

**Read:** `src/refast/components/shadcn/data_display.py`, `src/refast/components/shadcn/controls.py`

**Components to document:**
- `Table` / `TableHeader` / `TableBody` / `TableRow` / `TableHead` / `TableCell`
- `DataTable` — higher-level table (document if functional, note if not)
- `Avatar` — user avatar (src, alt, fallback)
- `Image` — responsive image (src, alt)
- `List` — ordered/unordered list
- `Calendar` — date calendar
- `Progress` — progress bar (value, max)
- `Skeleton` — loading placeholder (variant)
- `Carousel` / `CarouselContent` / `CarouselItem` / `CarouselPrevious` / `CarouselNext`
- `Accordion` / `AccordionItem` / `AccordionTrigger` / `AccordionContent` — (type single/multiple, collapsible)
- `Tabs` / `TabItem` — tabbed sections (default_value)
- `HoverCard` / `HoverCardTrigger` / `HoverCardContent`
- `Tooltip` — hover tooltip (content, side)

---

### 7. `navigation.py` — Navigation (`/docs/components/navigation`)

**Read:** `src/refast/components/shadcn/navigation.py`

**Components to document:**
- All Breadcrumb components
- All NavigationMenu components
- All Pagination components
- All Menubar components
- All Command components (command palette)
- All Sidebar components (22+ sub-components)

**Reference examples:** `examples/sidebar_showcase/app.py`, `examples/navigation_showcase/app.py`

---

### 8. `feedback.py` — Feedback & Overlay (`/docs/components/feedback`)

**Read:** `src/refast/components/shadcn/feedback.py`, `src/refast/components/shadcn/overlay.py`

**Components to document:**
- `Alert` — info/error alert (title, description, variant)
- `Spinner` — loading spinner (size)
- `Progress` — progress bar
- `Skeleton` — loading placeholder
- All Dialog components
- All Sheet components (side: top/right/bottom/left)
- All Drawer components
- All Popover components
- `Tooltip`
- `LoadingOverlay`

---

### 9. `charts.py` — Charts (`/docs/components/charts`)

**Read:** `src/refast/components/shadcn/charts.py`, `examples/charts_showcase/app.py`

**Components to document:**
- `ChartContainer` + `ChartConfig` + `ChartColor`
- `BarChart` + `Bar`
- `LineChart` + `Line`
- `AreaChart` + `Area`
- `PieChart` + `Pie` + `Cell`
- `RadarChart` + `Radar`
- `RadialChart` + `RadialBar`
- `ScatterChart` + `Scatter`
- Shared: `XAxis`, `YAxis`, `CartesianGrid`, `PolarGrid`, `PolarAngleAxis`, `PolarRadiusAxis`
- `ChartTooltip` / `ChartTooltipContent`
- `ChartLegend` / `ChartLegendContent`
- `ReferenceLine`

**Live demos:** Include at least one working chart per type

---

### 10. `utility.py` — Utility (`/docs/components/utility`)

**Read:** `src/refast/components/shadcn/icon.py`, `src/refast/components/shadcn/utility.py`, `src/refast/components/slot.py`

**Components to document:**
- `Icon` — Lucide icon (name, size). List all available icon names.
- `ThemeSwitcher` — light/dark/system toggle
- `ConnectionStatus` — WebSocket connection indicator
- `Slot` — dynamic content placeholder (id, fallback)
- `Empty` — renders nothing
- `LoadingOverlay` — full-screen loading overlay
- `Kbd` — keyboard shortcut display
