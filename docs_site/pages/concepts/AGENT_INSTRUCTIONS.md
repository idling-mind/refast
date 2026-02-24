# Core Concepts Section — Agent Instructions

## Section Goal

Explain **every core concept** a Refast developer needs to understand. Each page should
be self-contained but link to related concepts. Include code examples and, where useful,
live interactive demos using real Refast components.

---

## General Pattern for Each Page

1. **Overview** — What is this concept and why does it matter?
2. **Basic Usage** — Simplest possible working example
3. **Detailed API** — All methods/properties with a props table
4. **Patterns & Best Practices** — Common usage patterns
5. **Important Notes / Gotchas** — Edge cases, limitations
6. **Next Steps** — Links to related concept pages

---

## Pages

### 1. `components.py` — Components (`/docs/concepts/components`)

**Read:** `src/refast/components/base.py`

**Cover:**
- Component tree model — everything is a component, nested as children
- Base components: `Container` (div), `Text` (span), `Fragment` (no wrapper)
- Common props: `id`, `class_name`, `children`, `style`
- How `render()` produces JSON: `{"type": "...", "id": "...", "props": {...}, "children": [...]}`
- The `snake_case` → `camelCase` automatic conversion
- Component registry — how the frontend knows which React component to use

**Live demo:** Show a Container with nested Text, Heading, Badge to visualize the tree

---

### 2. `callbacks.py` — Callbacks & Events (`/docs/concepts/callbacks`)

**Read:** `src/refast/context.py` (callback/js methods, save_prop, chain), `src/refast/events/types.py`

**Cover:**
- `ctx.callback(func)` — creating a callback
- Bound arguments: `ctx.callback(func, item_id="abc")`
- Event props: `on_click`, `on_change`, `on_submit`, `on_checked_change`, `on_value_change`, `on_open_change`
- The callback lifecycle: user action → WebSocket → Python → response
- `save_prop` parameter — client-side form state without roundtrips. Reference prop in another callback.
- `js`, `bound_js` as callbacks
- Methods of ctx object like 
  - `show_toast`
  - `refresh`
  - `replace` 
  - `append` 
  - `prepend` 
  - `remove` 
  - `update_text`
  - `update_props`
  - `append_props`
  - `navigate`
  - `set_theme`
  - `push_event`
  - `broadcast`
  - `broadcase_theme`
- Events related to state and store will be handled separately.
- Debounce/throttle
- Error handling in callbacks

**Live demo:** A button that shows a toast, an input with `save_prop` that displays the stored value

---

### 3. `state.py` — State Management (`/docs/concepts/state`)

**Read:** `src/refast/state.py`

**Cover:**
- `ctx.state` — per-connection server-side dict
- `.get(key, default)`, `.set(key, value)`, `.update(dict)`, `.to_dict()`
- Bracket syntax: `ctx.state["key"]`
- Pattern: modify state → `ctx.refresh()` to re-render
- Lifecycle: state exists only within the WebSocket session
- State is NOT shared across tabs
- State vs Store comparison table

**Live demo:** A counter that increments on button click

---

### 4. `store.py` — Store (Browser Storage) (`/docs/concepts/store`)

**Read:** `src/refast/store.py`, `docs/PROP_STORE_GUIDE.md`, `examples/prop_store/app.py`

**Cover:**
- `ctx.store.local` (localStorage) and `ctx.store.session` (sessionStorage)
- Full API: `get`, `set`, `delete`, `clear`, `get_all`, `set_many`
- `store_as` on callbacks/inputs — client-side form state
- `ctx.prop_store` — reading stored values
- `ctx.sync_store()` — pulling latest values from browser
- When to use store vs state
- Store persists across page reloads; state doesn't

**Live demo:** Input with `store_as` that persists across refresh

---

### 5. `updates.py` — DOM Updates (`/docs/concepts/updates`)

**Read:** `src/refast/context.py` (replace/append/etc.), `examples/longrunning.py`

**Cover:**
- Full re-render: `ctx.refresh()`, `ctx.push_update()`
- Targeted updates (all require `id` on target):
  - `ctx.replace(id, component)` — swap entire element
  - `ctx.append(id, component)` — add child at end
  - `ctx.prepend(id, component)` — add child at beginning
  - `ctx.remove(id)` — delete element
  - `ctx.update_props(id, props)` — change specific props
  - `ctx.update_text(id, text)` — change text content
  - `ctx.append_prop(id, prop, value)` — append to list prop
- Performance comparison table
- When to use which approach

**Live demo:** A list where items can be appended/removed with targeted updates

---

### 6. `routing.py` — Routing & Navigation (`/docs/concepts/routing`)

**Read:** `examples/multi_page/app.py`, `src/refast/router.py`

**Cover:**
- `@ui.page("/path")` — registering pages
- `ctx.navigate("/path")` — SPA navigation
- `ctx.refresh()` / `ctx.refresh("/path")` — re-rendering
- How SPA navigation works internally (JSON fetch + tree swap)
- State persistence across navigations (same WebSocket)
- `Link` component for declarative navigation
- No wildcard routes — each page registered explicitly

---

### 7. `streaming.py` — Streaming (`/docs/concepts/streaming`)

**Read:** `docs/STREAMING_GUIDE.md`, `examples/streaming/app.py`, `src/refast/events/stream.py`

**Cover:**
- `async with ctx.stream(target_id) as stream:` — context manager
- `stream.send(chunk)` — incremental text updates
- Streaming to `Text` and `Markdown` components
- Performance tips (chunk size, batching)
- Use cases: LLM output, logs, progress text

**Live demo:** A button that triggers streaming text output

---

### 8. `background.py` — Background Jobs & Broadcasting (`/docs/concepts/background`)

**Read:** `examples/realtime_dashboard/app.py`, `src/refast/events/broadcast.py`

**Cover:**
- `asyncio.create_task()` for background work
- `ui.active_contexts` — all connected WebSocket contexts
- Broadcasting pattern: iterate contexts, push updates to each
- FastAPI lifespan for app-lifetime tasks
- `ctx.broadcast(event_type, data)` — broadcast custom events
- `ctx.push_event(event_type, data)` — push to current client
- Handling disconnections gracefully

---

### 9. `theming.py` — Theming (`/docs/concepts/theming`)

**Read:** `src/refast/theme/theme.py`, `src/refast/theme/defaults.py`, `examples/theme_showcase/app.py`

**Cover:**
- `Theme` class with `light` and `dark` `ThemeColors`
- 8 built-in presets: blue, rose, green, orange, violet, slate, zinc (+ default)
- `RefastApp(theme=slate_theme)` — applying at startup
- `ctx.set_theme(theme)` — runtime switch for current client
- `ctx.broadcast_theme(theme)` — switch for all clients
- `ThemeSwitcher` component — light/dark/system toggle
- CSS custom properties and HSL color tokens
- Custom theme creation with `ThemeColors`

**Live demo:** Theme switcher dropdown that changes the page theme

---

### 10. `toasts.py` — Toast Notifications (`/docs/concepts/toasts`)

**Read:** `examples/toast_showcase/app.py`

**Cover:**
- `ctx.show_toast(message, variant, ...)` — full API
- Variants: default, success, error, warning, info, loading
- All parameters: description, duration, position, dismissible, close_button, invert, action, cancel, toast_id
- Updating an existing toast by ID
- Position options (6 positions)

**Live demo:** Buttons for each toast variant that trigger actual toasts on click

---

### 11. `js_interop.py` — JavaScript Interop (`/docs/concepts/js-interop`)

**Read:** `examples/js_callbacks/app.py`, `src/refast/context.py`

**Cover:**
- `ctx.js(code)` — client-side callback (no server roundtrip)
- `ctx.bound_js(target_id, method, *args)` — call method on element
- `ctx.call_js(code)` — immediate execution from Python
- `ctx.call_bound_js(target_id, method, *args)` — immediate bound call
- Comparison table: when to use JS vs Python callbacks
- Security considerations
- Interacting with browser APIs (clipboard, geolocation, etc.)
