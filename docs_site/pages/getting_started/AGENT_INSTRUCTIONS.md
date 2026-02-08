# Getting Started Section — Agent Instructions

## Section Goal

Get a new user from **zero to running their first Refast app** in under 5 minutes.
These pages should be welcoming, practical, and code-heavy with working examples.

---

## Pages

### 1. `installation.py` — Installation & Getting Started (`/docs/getting-started`)

**Content Requirements:**
- Prerequisites: Python 3.11+, FastAPI knowledge helpful but not required
- Installation via pip and uv
- Create a minimal "hello world" app (5 lines)
- Run with uvicorn
- What each line does (annotated walkthrough)
- Project structure recommendations for larger apps
- Link to Architecture and Quick Tour as next steps

**Source files to read:**
- `examples/hello.py` — simplest possible app
- `examples/basic/app.py` — slightly more complex with callbacks
- `src/refast/app.py` — RefastApp constructor signature and defaults
- `pyproject.toml` — dependency list

**Live examples to include:**
- None needed (this is a text-heavy getting started guide)

---

### 2. `architecture.py` — Architecture (`/docs/architecture`)

**Content Requirements:**
- High-level diagram: Python → JSON → React → WebSocket → Python
- The HTML shell: what's in it (theme CSS, client bundle, component tree JSON)
- Initial page load flow (HTTP GET)
- WebSocket connection and event loop
- SPA navigation flow (ctx.navigate → JSON fetch → tree swap)
- Static asset serving (`/static/refast-client.js`, `/static/refast-client.css`)
- Component serialization: Python objects → JSON → React rendering
- Key classes table: RefastApp, Context, State, Store, Component, EventManager

**Source files to read:**
- `src/refast/app.py` — `_render_page()` method, HTML template
- `src/refast/router.py` — Route registration, WebSocket handler
- `src/refast/context.py` — Context class overview
- `src/refast/events/stream.py` — WebSocket stream management
- `src/refast/components/base.py` — Component.render() → dict

**Live examples to include:**
- None (conceptual/diagram page)

---

### 3. `quick_tour.py` — Quick Tour (`/docs/quick-tour`)

**Content Requirements:**
- Step-by-step walkthrough building a todo app
- Step 1: Create the app instance and FastAPI integration
- Step 2: Define a page with `@ui.page("/")`
- Step 3: Build the UI with Container, Input, Button, Checkbox
- Step 4: Add state management with `ctx.state`
- Step 5: Create callbacks for add, toggle, delete
- Step 6: Use `store_as` for the input field
- Step 7: Run and test
- Complete code at the end
- "What you learned" summary linking to concept pages

**Source files to read:**
- `examples/todo_app/app.py` — the working todo example to base this on

**Live examples to include:**
- Optionally embed a mini working example (a simplified counter) using real components

---

### 4. `examples_gallery.py` — Examples Gallery (`/docs/examples`)

**Content Requirements:**
- Grid of cards, one per example app
- Each card: title, icon, description, source file path
- Group by complexity/topic if desired
- Brief description of what each example demonstrates
- Note that examples can be run with `uvicorn examples.<name>.app:app --reload`

**Source files to read:**
- All `examples/*/README.md` files for descriptions
- All `examples/*/app.py` files for brief review

**Note:** This page already has a good initial implementation with the EXAMPLES list.
The agent should verify descriptions match the actual example code and enrich them.
