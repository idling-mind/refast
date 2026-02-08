# Refast Documentation Site — Agent Instructions

## Project Overview

This is a **documentation site for the Refast framework**, built using Refast itself (dogfooding).
It runs as a standard Refast app with a sidebar-based layout and 30+ pages of documentation.

## How to Run

```bash
cd <project_root>
uvicorn docs_site.app:app --reload --port 8000
```

Open http://localhost:8000 in your browser.

## Architecture

- **`app.py`** — Main app. Contains `RefastApp`, shared `docs_layout()` function, all route registrations.
- **`pages/`** — Each page is a Python module with a `render(ctx)` function.
- **Navigation** — Sidebar with 4 sections (Getting Started, Concepts, Components, Advanced). SPA navigation via `ctx.navigate()`.
- **Content** — Primarily `Markdown(text="""...""")` blocks for prose, with real Refast components for live examples.

## Content Format Rules

1. **Page structure**: Every page's `render(ctx)` returns `docs_layout(ctx, content, PAGE_ROUTE)` where content is wrapped in `Container(class_name="max-w-4xl mx-auto p-6", children=[...])`.
2. **Title**: Start with `Heading(PAGE_TITLE, level=1)` followed by `Separator(class_name="my-4")`.
3. **Prose**: Use `Markdown(text="""...""")` for body text, tables, code blocks.
4. **Live examples**: Embed actual Refast components alongside their code snippets so readers see both the code and the rendered result.
5. **Callouts**: Use `Alert(title="...", description="...")` for important notes.
6. **Code examples**: Use triple-backtick code blocks inside the Markdown text. The Markdown component supports syntax highlighting.
7. **Cross-links**: Reference other pages by their routes (e.g., `[State Management](/docs/concepts/state)`).

## Adding a New Page

1. Create `pages/<section>/<page_name>.py` with `PAGE_TITLE`, `PAGE_ROUTE`, and `render(ctx)`.
2. In `app.py`, import the module and add a `@ui.page(route)` handler.
3. Add the page to `NAV_SECTIONS` in `app.py` so it appears in the sidebar.

## Available Components for Documentation

From `refast.components`: Container, Flex, Row, Column, Grid, Center, Heading, Text, Paragraph, Code, Link, Markdown, Badge, Icon, Button, Card, CardHeader, CardTitle, CardDescription, CardContent, CardFooter, Tabs, TabItem, Accordion, AccordionItem, AccordionTrigger, AccordionContent, Alert, Separator, Table, TableHeader, TableBody, TableRow, TableHead, TableCell, and many more.

## Source Files Reference

When writing documentation content, read these source files for accuracy:

| Topic | Source Files |
|-------|-------------|
| App & Router | `src/refast/app.py`, `src/refast/router.py` |
| Context | `src/refast/context.py` |
| State | `src/refast/state.py` |
| Store | `src/refast/store.py` |
| Components (base) | `src/refast/components/base.py` |
| Components (shadcn) | `src/refast/components/shadcn/*.py` |
| Events | `src/refast/events/types.py`, `src/refast/events/manager.py` |
| Streaming | `src/refast/events/stream.py` |
| Broadcasting | `src/refast/events/broadcast.py` |
| Sessions | `src/refast/session/` |
| Security | `src/refast/security/` |
| Theme | `src/refast/theme/` |
| Extensions | `src/refast/extensions/` |
| Examples | `examples/` (25+ working examples) |
| Existing docs | `docs/*.md` |

## Known Issues

See `TODO.md` in this directory for tracked issues found during development.

## Section-Specific Instructions

Each section folder has its own `AGENT_INSTRUCTIONS.md` with per-page content requirements:

- `pages/getting_started/AGENT_INSTRUCTIONS.md`
- `pages/concepts/AGENT_INSTRUCTIONS.md`
- `pages/components/AGENT_INSTRUCTIONS.md`
- `pages/advanced/AGENT_INSTRUCTIONS.md`
