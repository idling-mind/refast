# Architecture Improvements

Deepening opportunities identified via architectural review (2026-05-10).
Working through these one by one, top to bottom.

---

## 1. Callback registry per-connection, not per-app — ✅ Done

**Files**: `src/refast/context.py`, `src/refast/app.py`, `src/refast/router.py`

**Problem**: Every call to `ctx.callback(fn)` generates a new UUID and immediately
registers `fn` into `app._callbacks` — a dict on the `RefastApp` instance. This dict is
never pruned. Every page re-render (on `store_init`, `navigate`, `ctx.refresh()`) adds a
fresh batch of callbacks with new UUIDs; old callbacks from previous renders remain
registered indefinitely, growing without bound for the lifetime of the process.
Old callbacks also remain dispatchable from stale frontend state.

**Solution**: Move the callback dict off the app and onto `Context`.
The router already keeps one `Context` per `WebSocket`; that context owns its callback
map and clears it each time a new page is rendered.
The app needs no callback state at all.

**Benefits**:
- Locality — registration, lookup, and cleanup are all on the same object.
- Leverage — tests can create a `Context` in isolation and assert its callbacks without a full `RefastApp`.
- Safety — stale callbacks from previous renders cannot be dispatched after a navigation.

---

## 2. WebSocket message dispatcher — ✅ Done

**Files**: `src/refast/router.py` (`_handle_websocket_message`)

**Problem**: One ~200-line method handles five unrelated message types (`callback`,
`store_init`, `navigate`, `event`, `store_sync`), plus does inline `inspect.signature`
parameter filtering. Adding a new message type means editing this method.
The callback dispatch logic is buried inside routing code, making it untestable
without a live WebSocket.

**Solution**: Extract a message dispatcher — a registry mapping message type strings to
dedicated handler coroutines. The inline `inspect.signature` parameter filtering
(deciding which kwargs a callback accepts) moves to a helper that can be unit-tested
with just a function and a dict.

**Benefits**:
- Locality — each message type's logic is in one place.
- Leverage — a new message type is a new registration, not a new branch.
- The parameter-filtering logic can be tested without a live WebSocket.

---

## 3. Action types extracted from context.py — ✅ Done

**Files**: `src/refast/context.py`

**Problem**: `context.py` is ~700 lines because it contains both the `Context` class and
five independent dataclasses (`Callback`, `JsCallback`, `BoundJsCallback`, `SaveProp`,
`ChainedAction`). Each dataclass independently duplicates `debounce: int = 0`,
`throttle: int = 0`, and the serialization logic for those fields.
Anything importing only `Callback` must import from the entire `Context` module.

**Solution**: Extract the action dataclasses to `src/refast/events/actions.py`.
Add a common base carrying `debounce`/`throttle` and a shared `_serialize_timing()`
helper. Re-export from `context.py` for backward compatibility.

**Benefits**:
- Locality — all action types and their shared invariants are in one module.
- Leverage — `context.py` shrinks to its actual job (per-request state and action creation).
- Callers that only need `Callback` or `SaveProp` do not import `Context`.

---

## 4. Asset pipeline extracted from router.py — ✅ Done

**Files**: `src/refast/router.py`

**Problem**: `router.py` conflates HTTP/WebSocket routing with an asset pipeline —
manifest parsing, Vite chunk inference, HTML shell generation, pre-compressed file
negotiation, and MIME type sanitization. The manifest-walking logic (`_get_chunk_files`)
is a non-trivial recursive tree walk; `_render_html_shell` is a 100+-line string
template. Neither can be tested without pulling in the router.

**Solution**: Extract `src/refast/assets.py` (or `static_assets.py`) owning
`ALL_FEATURE_CHUNKS`, manifest loading, chunk resolution, and HTML shell rendering.
`RefastRouter` uses it as a dependency. File-serving handlers can also be extracted.

**Benefits**:
- Locality — Vite manifest logic, feature-chunk inference, and HTML shell template are together.
- Leverage — the asset pipeline is testable with fixture manifests, no router needed.
- Changes to the chunk naming scheme land in one file.

---

## 5. Component tree operations formalized — ✅ Done

**Files**: `src/refast/utils/component.py`, `src/refast/context.py`

**Problem**: The only formalized tree operation is `find_component_in_tree`, a recursive
function using `getattr(root, "_children", [])` (duck typing) with a hard-coded special
case for `Slot.fallback`. Adding a new operation (remove, find-by-type, walk-all-callbacks)
requires touching multiple files. The `ctx.refresh()`, `ctx.replace()`, `ctx.append()`
methods each do their own traversal with no shared abstraction.

**Solution**: Formalize a `ComponentTree` module with a clear interface:
`find(root, id)`, `replace(root, id, component)`, `append_children(root, id, children)`,
`walk(root, visitor)`. Move the `fallback` special-casing inside `Component` via a
`_traversal_children()` override, so the tree walker has no component-type knowledge.
Context methods become thin wrappers over the tree module + WebSocket send.

**Benefits**:
- Locality — all tree navigation and special cases in one module.
- Leverage — new operations reuse the traversal; no new duck-typing loops needed.
- Visitor pattern enables future operations (serialization, validation, ID collection) without new traversals.
