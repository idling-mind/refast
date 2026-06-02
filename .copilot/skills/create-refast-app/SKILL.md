---
name: create-refast-app
description: Guide for creating, scaffolding, and extending a Refast application. Use this when asked to build pages, add components, handle events, implement streaming, or structure a multi-page app.
---

# Skill: Create a Refast App

**Use this skill** when the user asks to build, scaffold, extend, or debug a Refast application — including creating pages, adding components, handling events, implementing streaming, or structuring a multi-page app.

Refast is a Python + React framework where you write Python-only application code. FastAPI serves as the backend; a compiled React frontend renders the UI. The two layers communicate over a persistent WebSocket.

---

## Skill Files (read when relevant)

| File | Contents |
|------|----------|
| [01-core-setup.md](./01-core-setup.md) | App creation, pages, Context API, state management, startup |
| [02-components-layout.md](./02-components-layout.md) | All built-in components with props and usage examples |
| [03-events-callbacks.md](./03-events-callbacks.md) | Callbacks, prop store, chains, JS interop, forms |
| [04-streaming-advanced.md](./04-streaming-advanced.md) | Streaming output, long-running tasks, broadcast/realtime |
| [05-navigation-structure.md](./05-navigation-structure.md) | Multi-page routing, sidebar layout, shared layout patterns |

---

## Quick Orientation

```python
# Minimal working app
from fastapi import FastAPI
from refast import RefastApp, Context
from refast import components as rc

ui = RefastApp(title="My App")

@ui.page("/")
def home(ctx: Context):
    return rc.Container(children=[
        rc.Heading("Hello, Refast!", level=1),
        rc.Button("Click me", on_click=ctx.callback(handle_click)),
    ])

async def handle_click(ctx: Context):
    await ctx.show_toast("Button clicked!", variant="success")

app = FastAPI()
app.include_router(ui.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

---

## Key Mental Model

1. **Page functions are sync** — they return a component tree. Run on initial page load and on `await ctx.refresh()`.
2. **Callbacks are async** — they mutate `ctx.state`, then push targeted DOM updates back to the browser.
3. **Components have `id`s** — assign `id="my-id"` to any component to target it with `ctx.replace()`, `ctx.append()`, `ctx.update_props()`, etc.
4. **Prop store** — use `ctx.save_prop("key")` on input `on_change` to capture values client-side without a server roundtrip; retrieve them via `ctx.callback(fn, props=["key"])`.
5. **State lifetime** — `ctx.state` lives for the WebSocket connection. Use `ctx.store.local` for browser-persistent data.

---

## When to Read Which File

- **Starting from scratch / app structure** → read `01-core-setup.md`
- **Choosing or using a component** → read `02-components-layout.md`
- **Handling user input / forms** → read `03-events-callbacks.md`
- **AI output, live charts, long tasks** → read `04-streaming-advanced.md`
- **Adding pages, sidebar nav, breadcrumbs** → read `05-navigation-structure.md`
