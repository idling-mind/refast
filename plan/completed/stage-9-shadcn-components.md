# Stage 9: Comprehensive shadcn/ui Components

## Progress

- [ ] Phase 1: Radix UI Primitives Integration
- [ ] Phase 2: Navigation Components
- [ ] Phase 3: Overlay Components
- [ ] Phase 4: Form Components (Advanced)
- [ ] Phase 5: Data Display Components (Advanced)
- [ ] Phase 6: Layout Components (Advanced)
- [ ] Phase 7: Utility Components

## Objectives

Implement a comprehensive set of shadcn/ui components to provide feature parity with https://ui.shadcn.com/docs/components.

This stage adds:
- Integration with @radix-ui primitives for accessibility
- Navigation components (Breadcrumb, NavigationMenu, Pagination, etc.)
- Overlay components (Dialog, Sheet, Popover, etc.)
- Advanced form controls (DatePicker, Combobox, Slider, etc.)
- Advanced data display (DataTable with sorting/filtering, Carousel, etc.)

## Prerequisites

- Stage 6 complete (React frontend)
- Stage 7 complete (Integration)

## Current Components (Already Implemented)

### Python Backend (`src/refast/components/shadcn/`)
| Component | File | Notes |
|-----------|------|-------|
| Button, IconButton | button.py | ✅ Complete |
| Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter | card.py | ✅ Complete |
| Input, Checkbox, Radio, Select, Textarea | input.py | ✅ Complete |
| Form, FormField, Label | form.py | ✅ Complete |
| Row, Column, Stack, Grid, Flex, Center, Spacer, Divider | layout.py | ✅ Complete |
| Heading, Paragraph, Link, Code | typography.py | ✅ Complete |
| Alert, Dialog, Modal, Progress, Skeleton, Spinner, Toast | feedback.py | ✅ Complete |
| Accordion, Avatar, Badge, DataTable, List, Table, Tabs, TabItem, Tooltip | data_display.py | ✅ Complete |

### React Frontend (`src/refast-client/src/components/shadcn/`)
| Component | File | Notes |
|-----------|------|-------|
| Button, IconButton | button.tsx | ✅ Complete |
| Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter | card.tsx | ✅ Complete |
| Input, Textarea, Select, SelectOption, Checkbox, Radio, RadioGroup | input.tsx | ✅ Complete |
| Row, Column, Stack, Grid, Flex, Center, Spacer, Divider | layout.tsx | ✅ Complete |
| Heading, Paragraph, Link, Code, BlockQuote, List, ListItem, Label | typography.tsx | ✅ Complete |
| Alert, AlertTitle, AlertDescription, Badge, Progress, Spinner, Toast, Skeleton | feedback.tsx | ✅ Complete |
| Table, TableHeader, TableBody, TableRow, TableHead, TableCell, Avatar, Image, Tooltip | data_display.tsx | ✅ Complete |
| Slot | slot.tsx | ✅ Complete |

---

## Phase 1: Radix UI Primitives Integration

### Description
Upgrade existing components to use @radix-ui primitives for better accessibility and behavior.

### Dependencies to Add
```json
{
  "@radix-ui/react-accordion": "^1.2.0",
  "@radix-ui/react-alert-dialog": "^1.1.0",
  "@radix-ui/react-aspect-ratio": "^1.1.0",
  "@radix-ui/react-avatar": "^1.1.0",
  "@radix-ui/react-checkbox": "^1.1.0",
  "@radix-ui/react-collapsible": "^1.1.0",
  "@radix-ui/react-context-menu": "^2.2.0",
  "@radix-ui/react-dialog": "^1.1.0",
  "@radix-ui/react-dropdown-menu": "^2.1.0",
  "@radix-ui/react-hover-card": "^1.1.0",
  "@radix-ui/react-label": "^2.1.0",
  "@radix-ui/react-menubar": "^1.1.0",
  "@radix-ui/react-navigation-menu": "^1.2.0",
  "@radix-ui/react-popover": "^1.1.0",
  "@radix-ui/react-progress": "^1.1.0",
  "@radix-ui/react-radio-group": "^1.2.0",
  "@radix-ui/react-scroll-area": "^1.1.0",
  "@radix-ui/react-select": "^2.1.0",
  "@radix-ui/react-separator": "^1.1.0",
  "@radix-ui/react-slider": "^1.2.0",
  "@radix-ui/react-switch": "^1.1.0",
  "@radix-ui/react-tabs": "^1.1.0",
  "@radix-ui/react-toast": "^1.2.0",
  "@radix-ui/react-toggle": "^1.1.0",
  "@radix-ui/react-toggle-group": "^1.1.0",
  "@radix-ui/react-tooltip": "^1.1.0"
}
```

### Tasks

#### Task 1.1: Upgrade Accordion
- Migrate to `@radix-ui/react-accordion`
- Add keyboard navigation
- Add animation support

#### Task 1.2: Upgrade Avatar
- Migrate to `@radix-ui/react-avatar`
- Add fallback support
- Add image loading states

#### Task 1.3: Upgrade Checkbox
- Migrate to `@radix-ui/react-checkbox`
- Add indeterminate state
- Improve accessibility

#### Task 1.4: Upgrade Dialog/Modal
- Migrate to `@radix-ui/react-dialog`
- Add portal support
- Add focus trap

#### Task 1.5: Upgrade Progress
- Migrate to `@radix-ui/react-progress`
- Add indeterminate state
- Add animation

#### Task 1.6: Upgrade Radio
- Migrate to `@radix-ui/react-radio-group`
- Improve keyboard navigation

#### Task 1.7: Upgrade Select
- Migrate to `@radix-ui/react-select`
- Add search/filter
- Add groups

#### Task 1.8: Upgrade Tabs
- Migrate to `@radix-ui/react-tabs`
- Add keyboard navigation
- Add orientation support

#### Task 1.9: Upgrade Tooltip
- Migrate to `@radix-ui/react-tooltip`
- Add delay controls
- Add positioning

### Tests
- Unit tests for each upgraded component
- Accessibility tests (keyboard navigation, screen readers)
- Visual regression tests

---

## Phase 2: Navigation Components

### Description
Add navigation-related components from shadcn/ui.

### Components to Implement

#### 2.1: Breadcrumb
A navigation component showing the current page location.

**Python API:**
```python
from refast.components import Breadcrumb, BreadcrumbItem, BreadcrumbLink, BreadcrumbSeparator

Breadcrumb(
    BreadcrumbItem(BreadcrumbLink("Home", href="/")),
    BreadcrumbSeparator(),
    BreadcrumbItem(BreadcrumbLink("Components", href="/components")),
    BreadcrumbSeparator(),
    BreadcrumbItem("Breadcrumb", current=True),
)
```

**Files:**
- `src/refast/components/shadcn/navigation.py`
- `src/refast-client/src/components/shadcn/navigation.tsx`

#### 2.2: NavigationMenu
A collection of links for navigating websites.

**Python API:**
```python
from refast.components import NavigationMenu, NavigationMenuItem, NavigationMenuTrigger, NavigationMenuContent

NavigationMenu(
    NavigationMenuItem(
        NavigationMenuTrigger("Getting Started"),
        NavigationMenuContent(
            Link("Introduction", href="/docs"),
            Link("Installation", href="/docs/install"),
        ),
    ),
)
```

#### 2.3: Pagination
A component for paginating through content.

**Python API:**
```python
from refast.components import Pagination, PaginationContent, PaginationItem, PaginationLink, PaginationPrevious, PaginationNext, PaginationEllipsis

Pagination(
    PaginationContent(
        PaginationItem(PaginationPrevious(href="#")),
        PaginationItem(PaginationLink("1", href="#", active=True)),
        PaginationItem(PaginationLink("2", href="#")),
        PaginationItem(PaginationEllipsis()),
        PaginationItem(PaginationNext(href="#")),
    ),
)
```

#### 2.4: Sidebar
A composable sidebar component.

**Python API:**
```python
from refast.components import Sidebar, SidebarContent, SidebarGroup, SidebarGroupLabel, SidebarGroupContent, SidebarMenu, SidebarMenuItem, SidebarMenuButton

Sidebar(
    SidebarContent(
        SidebarGroup(
            SidebarGroupLabel("Application"),
            SidebarGroupContent(
                SidebarMenu(
                    SidebarMenuItem(SidebarMenuButton("Dashboard", icon="Home")),
                    SidebarMenuItem(SidebarMenuButton("Settings", icon="Settings")),
                ),
            ),
        ),
    ),
)
```

#### 2.5: Menubar
A visually persistent menu common in desktop applications.

**Python API:**
```python
from refast.components import Menubar, MenubarMenu, MenubarTrigger, MenubarContent, MenubarItem

Menubar(
    MenubarMenu(
        MenubarTrigger("File"),
        MenubarContent(
            MenubarItem("New Tab", shortcut="⌘T"),
            MenubarItem("New Window", shortcut="⌘N"),
        ),
    ),
)
```

#### 2.6: Command
A command menu component (CMD+K style).

**Python API:**
```python
from refast.components import Command, CommandInput, CommandList, CommandEmpty, CommandGroup, CommandItem

Command(
    CommandInput(placeholder="Type a command..."),
    CommandList(
        CommandEmpty("No results found."),
        CommandGroup(
            heading="Suggestions",
            CommandItem("Calendar", icon="Calendar"),
            CommandItem("Search", icon="Search"),
        ),
    ),
)
```

### Tests
- Navigation keyboard accessibility
- Active state management
- Mobile responsive behavior

---

## Phase 3: Overlay Components

### Description
Add overlay/modal components that appear above the page content.

### Components to Implement

#### 3.1: AlertDialog
A modal dialog that interrupts the user with important content.

**Python API:**
```python
from refast.components import AlertDialog, AlertDialogTrigger, AlertDialogContent, AlertDialogHeader, AlertDialogTitle, AlertDialogDescription, AlertDialogFooter, AlertDialogAction, AlertDialogCancel

AlertDialog(
    AlertDialogTrigger(Button("Delete")),
    AlertDialogContent(
        AlertDialogHeader(
            AlertDialogTitle("Are you absolutely sure?"),
            AlertDialogDescription("This action cannot be undone."),
        ),
        AlertDialogFooter(
            AlertDialogCancel("Cancel"),
            AlertDialogAction("Continue"),
        ),
    ),
)
```

#### 3.2: Sheet
A panel that slides out from the edge of the screen.

**Python API:**
```python
from refast.components import Sheet, SheetTrigger, SheetContent, SheetHeader, SheetTitle, SheetDescription, SheetFooter

Sheet(
    side="right",  # "top" | "right" | "bottom" | "left"
    SheetTrigger(Button("Open")),
    SheetContent(
        SheetHeader(
            SheetTitle("Edit Profile"),
            SheetDescription("Make changes to your profile."),
        ),
        # Form content here
        SheetFooter(Button("Save changes")),
    ),
)
```

#### 3.3: Popover
Displays rich content in a portal, triggered by a button.

**Python API:**
```python
from refast.components import Popover, PopoverTrigger, PopoverContent

Popover(
    PopoverTrigger(Button("Open popover")),
    PopoverContent(
        Heading("Dimensions", level=4),
        Paragraph("Set the dimensions for the layer."),
    ),
)
```

#### 3.4: HoverCard
For sighted users to preview content behind a link.

**Python API:**
```python
from refast.components import HoverCard, HoverCardTrigger, HoverCardContent

HoverCard(
    HoverCardTrigger(Link("@shadcn", href="#")),
    HoverCardContent(
        Avatar(src="...", alt="@shadcn"),
        Heading("@shadcn", level=4),
        Paragraph("The React Framework"),
    ),
)
```

#### 3.5: DropdownMenu
Displays a menu to the user, triggered by a button.

**Python API:**
```python
from refast.components import DropdownMenu, DropdownMenuTrigger, DropdownMenuContent, DropdownMenuItem, DropdownMenuSeparator, DropdownMenuLabel

DropdownMenu(
    DropdownMenuTrigger(Button("Open")),
    DropdownMenuContent(
        DropdownMenuLabel("My Account"),
        DropdownMenuSeparator(),
        DropdownMenuItem("Profile", shortcut="⇧⌘P"),
        DropdownMenuItem("Settings", shortcut="⌘S"),
        DropdownMenuSeparator(),
        DropdownMenuItem("Log out"),
    ),
)
```

#### 3.6: ContextMenu
Displays a menu on right-click.

**Python API:**
```python
from refast.components import ContextMenu, ContextMenuTrigger, ContextMenuContent, ContextMenuItem

ContextMenu(
    ContextMenuTrigger(
        Container("Right click here", class_name="border-2 border-dashed p-10")
    ),
    ContextMenuContent(
        ContextMenuItem("Back"),
        ContextMenuItem("Forward"),
        ContextMenuItem("Reload"),
    ),
)
```

#### 3.7: Drawer
A drawer component for mobile (using Vaul).

**Python API:**
```python
from refast.components import Drawer, DrawerTrigger, DrawerContent, DrawerHeader, DrawerTitle, DrawerDescription, DrawerFooter

Drawer(
    DrawerTrigger(Button("Open Drawer")),
    DrawerContent(
        DrawerHeader(
            DrawerTitle("Move Goal"),
            DrawerDescription("Set your daily activity goal."),
        ),
        # Content
        DrawerFooter(Button("Submit")),
    ),
)
```

### Dependencies
```json
{
  "vaul": "^0.9.0"
}
```

### Tests
- Portal rendering
- Focus management
- Escape key handling
- Click outside handling
- Animation states

---

## Phase 4: Form Components (Advanced)

### Description
Add advanced form controls from shadcn/ui.

### Components to Implement

#### 4.1: Switch
A toggle switch component.

**Python API:**
```python
from refast.components import Switch

Switch(
    id="airplane-mode",
    checked=True,
    on_change=ctx.callback(handle_change),
)
```

#### 4.2: Slider
A slider input for selecting a value from a range.

**Python API:**
```python
from refast.components import Slider

Slider(
    value=[50],
    min=0,
    max=100,
    step=1,
    on_value_change=ctx.callback(handle_change),
)
```

#### 4.3: Toggle
A two-state button that can be on or off.

**Python API:**
```python
from refast.components import Toggle

Toggle(
    "Bold",
    icon="Bold",
    pressed=True,
    on_pressed_change=ctx.callback(handle_toggle),
)
```

#### 4.4: ToggleGroup
A set of two-state buttons that can be toggled on or off.

**Python API:**
```python
from refast.components import ToggleGroup, ToggleGroupItem

ToggleGroup(
    type="single",  # "single" | "multiple"
    ToggleGroupItem("Bold", icon="Bold", value="bold"),
    ToggleGroupItem("Italic", icon="Italic", value="italic"),
    ToggleGroupItem("Underline", icon="Underline", value="underline"),
)
```

#### 4.5: Calendar
A date picker calendar component.

**Python API:**
```python
from refast.components import Calendar

Calendar(
    mode="single",  # "single" | "multiple" | "range"
    selected=date(2024, 1, 15),
    on_select=ctx.callback(handle_select),
)
```

**Dependencies:**
```json
{
  "react-day-picker": "^9.0.0",
  "date-fns": "^3.0.0"
}
```

#### 4.6: DatePicker
A date picker with input and calendar.

**Python API:**
```python
from refast.components import DatePicker

DatePicker(
    value=date(2024, 1, 15),
    placeholder="Pick a date",
    on_change=ctx.callback(handle_date_change),
)
```

#### 4.7: Combobox
An autocomplete input with dropdown.

**Python API:**
```python
from refast.components import Combobox

Combobox(
    options=[
        {"value": "next", "label": "Next.js"},
        {"value": "react", "label": "React"},
        {"value": "vue", "label": "Vue"},
    ],
    placeholder="Select framework...",
    on_select=ctx.callback(handle_select),
)
```

#### 4.8: InputOTP
An input for one-time passwords.

**Python API:**
```python
from refast.components import InputOTP, InputOTPGroup, InputOTPSlot, InputOTPSeparator

InputOTP(
    max_length=6,
    InputOTPGroup(
        InputOTPSlot(index=0),
        InputOTPSlot(index=1),
        InputOTPSlot(index=2),
    ),
    InputOTPSeparator(),
    InputOTPGroup(
        InputOTPSlot(index=3),
        InputOTPSlot(index=4),
        InputOTPSlot(index=5),
    ),
)
```

**Dependencies:**
```json
{
  "input-otp": "^1.0.0"
}
```

### Tests
- Controlled/uncontrolled modes
- Keyboard accessibility
- Form validation integration
- Mobile input handling

---

## Phase 5: Data Display Components (Advanced)

### Description
Add advanced data display components.

### Components to Implement

#### 5.1: Carousel
A carousel with motion and swipe gestures.

**Python API:**
```python
from refast.components import Carousel, CarouselContent, CarouselItem, CarouselPrevious, CarouselNext

Carousel(
    CarouselContent(
        CarouselItem(Card(...)),
        CarouselItem(Card(...)),
        CarouselItem(Card(...)),
    ),
    CarouselPrevious(),
    CarouselNext(),
)
```

**Dependencies:**
```json
{
  "embla-carousel-react": "^8.0.0"
}
```

#### 5.2: Collapsible
A component that expands/collapses content.

**Python API:**
```python
from refast.components import Collapsible, CollapsibleTrigger, CollapsibleContent

Collapsible(
    CollapsibleTrigger(Button("Toggle")),
    CollapsibleContent(
        Paragraph("This content can be collapsed."),
    ),
)
```

#### 5.3: ScrollArea
A scrollable area with custom scrollbars.

**Python API:**
```python
from refast.components import ScrollArea, ScrollBar

ScrollArea(
    class_name="h-72 w-48",
    # Long content here
    ScrollBar(orientation="vertical"),
)
```

#### 5.4: Resizable
A resizable panel group.

**Python API:**
```python
from refast.components import ResizablePanelGroup, ResizablePanel, ResizableHandle

ResizablePanelGroup(
    direction="horizontal",
    ResizablePanel(default_size=50, Paragraph("One")),
    ResizableHandle(),
    ResizablePanel(default_size=50, Paragraph("Two")),
)
```

**Dependencies:**
```json
{
  "react-resizable-panels": "^2.0.0"
}
```

#### 5.5: AspectRatio
Displays content within a desired ratio.

**Python API:**
```python
from refast.components import AspectRatio

AspectRatio(
    ratio=16/9,
    Image(src="...", alt="Photo"),
)
```

#### 5.6: Separator
A visual separator.

**Python API:**
```python
from refast.components import Separator

Column(
    Heading("Title"),
    Separator(),
    Paragraph("Content below separator"),
)
```

#### 5.7: Sonner (Toast Notifications)
A toast notification system using Sonner.

**Python API:**
```python
from refast.components import Toaster
from refast import toast

# In layout
Toaster(position="bottom-right")

# In callback
async def handle_submit(ctx, event):
    toast.success("Profile updated!")
    toast.error("Something went wrong")
    toast.info("Did you know?")
```

**Dependencies:**
```json
{
  "sonner": "^1.4.0"
}
```

### Tests
- Animation states
- Responsive behavior
- Touch/swipe gestures
- Scroll performance

---

## Phase 6: Layout Components (Advanced)

### Description
Add additional layout utilities.

### Components to Implement

#### 6.1: AspectRatio
Already covered in Phase 5.

#### 6.2: Container
A max-width container with padding.

**Python API:**
```python
from refast.components import Container

Container(
    max_width="lg",  # "sm" | "md" | "lg" | "xl" | "2xl" | "full"
    centered=True,
    # Content
)
```

#### 6.3: Empty
An empty state component.

**Python API:**
```python
from refast.components import Empty

Empty(
    icon="Inbox",
    title="No messages",
    description="You don't have any messages yet.",
    action=Button("Send a message"),
)
```

### Tests
- Responsive breakpoints
- Max-width calculations

---

## Phase 7: Utility Components

### Description
Add utility components that enhance UX.

### Components to Implement

#### 7.1: Kbd
Keyboard key display.

**Python API:**
```python
from refast.components import Kbd

Paragraph("Press ", Kbd("⌘"), " + ", Kbd("K"), " to open command menu.")
```

#### 7.2: Skeleton
Already implemented - enhance with more variants.

#### 7.3: Loading States
Global loading state management.

**Python API:**
```python
from refast.components import LoadingOverlay, LoadingSpinner

# Page loading
LoadingOverlay(
    loading=ctx.state.is_loading,
    text="Loading...",
)
```

### Tests
- Animation performance
- Accessibility (aria-busy states)

---

## Implementation Priority

### High Priority (Commonly Used)
1. Switch
2. Slider
3. DropdownMenu
4. Sheet
5. Popover
6. Calendar/DatePicker
7. Separator
8. Breadcrumb

### Medium Priority
1. AlertDialog
2. HoverCard
3. ContextMenu
4. NavigationMenu
5. Combobox
6. Carousel
7. ScrollArea
8. Collapsible

### Lower Priority (Specialized)
1. Menubar
2. Command
3. Sidebar
4. InputOTP
5. Resizable
6. Drawer
7. Toggle/ToggleGroup

---

## File Structure

```
src/refast/components/shadcn/
├── __init__.py                 # Export all components
├── button.py                   # ✅ Existing
├── card.py                     # ✅ Existing
├── data_display.py             # ✅ Existing + enhancements
├── feedback.py                 # ✅ Existing + enhancements
├── form.py                     # ✅ Existing + enhancements
├── input.py                    # ✅ Existing + enhancements
├── layout.py                   # ✅ Existing + enhancements
├── typography.py               # ✅ Existing
├── navigation.py               # NEW: Breadcrumb, NavigationMenu, etc.
├── overlay.py                  # NEW: Sheet, Popover, DropdownMenu, etc.
├── controls.py                 # NEW: Switch, Slider, Toggle, etc.
├── calendar.py                 # NEW: Calendar, DatePicker
├── utility.py                  # NEW: Kbd, Separator, etc.

src/refast-client/src/components/shadcn/
├── button.tsx                  # ✅ Existing
├── card.tsx                    # ✅ Existing
├── data_display.tsx            # ✅ Existing + enhancements
├── feedback.tsx                # ✅ Existing + enhancements
├── input.tsx                   # ✅ Existing + enhancements
├── layout.tsx                  # ✅ Existing + enhancements
├── typography.tsx              # ✅ Existing
├── slot.tsx                    # ✅ Existing
├── navigation.tsx              # NEW
├── overlay.tsx                 # NEW
├── controls.tsx                # NEW
├── calendar.tsx                # NEW
├── utility.tsx                 # NEW
```

---

## Testing Strategy

### Unit Tests
- Each component has unit tests
- Test all props and variants
- Test controlled/uncontrolled modes

### Integration Tests
- Component composition
- Event handling through WebSocket
- State synchronization

### Accessibility Tests
- Keyboard navigation
- Screen reader announcements
- Focus management
- ARIA attributes

### Visual Tests
- Snapshot testing
- Storybook stories
- Responsive behavior

---

## Estimated Effort

| Phase | Components | Estimated Time |
|-------|------------|----------------|
| Phase 1 | 9 upgrades | 2-3 days |
| Phase 2 | 6 components | 3-4 days |
| Phase 3 | 7 components | 4-5 days |
| Phase 4 | 8 components | 4-5 days |
| Phase 5 | 7 components | 3-4 days |
| Phase 6 | 3 components | 1-2 days |
| Phase 7 | 3 components | 1 day |
| **Total** | **43 components** | **18-24 days** |

---

## Success Criteria

1. All components render correctly
2. All components pass accessibility audits
3. All components work with Python callbacks
4. All components have comprehensive tests
5. Documentation for each component
6. Example usage in the showcase app
