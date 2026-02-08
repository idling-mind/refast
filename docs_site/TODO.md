# Refast Documentation — Known Issues & TODOs

Issues discovered during documentation site development. Fix these in the framework
or document them as known limitations.

---

## Framework Issues

### 1. DataTable component may be non-functional
- **Location:** `src/refast/components/shadcn/data_display.py` → `DataTable`
- **Evidence:** `examples/data_table/app.py` builds tables manually from `Table`/`TableRow`/`TableCell` primitives rather than using the `DataTable` component
- **Action:** Verify if `DataTable` works. If not, either fix it or mark as experimental in docs.

### 2. Stage 8 plan uses outdated theme API
- **Location:** `plan/stage-8-docs.md`
- **Evidence:** References hex color constructors, but `Theme` now uses Pydantic `ThemeColors` with HSL tokens
- **Action:** Update the plan file or mark as superseded.

### 3. `style` prop usage inconsistency
- **Location:** `.github/copilot-instructions.md` says "No inline styles" but `docs/STYLING_GUIDE.md` explicitly documents `style` as supported for dynamic values
- **Evidence:** Several examples use `style={"display": "none"}` for conditional visibility
- **Action:** Clarify the guideline — `style` is fine for dynamic values, not for static styling.

### 4. No wildcard/catch-all route support
- **Evidence:** `examples/multi_page/app.py` and all examples register each page explicitly. No `@ui.page("/docs/*")` pattern exists.
- **Action:** Document as a known limitation. Consider implementing wildcard routes.

### 5. `ctx.state` unavailable on initial HTTP GET
- **Evidence:** Page handlers run for both HTTP GET (initial load) and within WebSocket context. On HTTP GET, there's no persistent state — `ctx.state` is empty.
- **Action:** Document clearly that state is only meaningful within callback/WebSocket context. Recommend using `ctx.store` for initial-load-required values.

### 6. Markdown component capabilities underdocumented
- **Evidence:** The `Markdown` component supports GFM (tables, strikethrough), syntax highlighting (via react-syntax-highlighter), and KaTeX math equations. None of this is mentioned in existing documentation.
- **Action:** Document all Markdown features in the Typography components reference page.

---

## Documentation TODOs

### Content Completion

All pages currently have placeholder content marked with `> **TODO**`. Each needs to be
fleshed out per the `AGENT_INSTRUCTIONS.md` in its section folder.

**Priority order for content writing:**

1. Getting Started section (installation, architecture, quick tour)
2. Core Concepts (callbacks, state, store, updates)
3. Component Reference (layout, buttons, inputs — most used)
4. Advanced topics (component dev, extension dev)
5. Remaining component pages (navigation, charts, etc.)

### Live Examples

Many component reference pages need live interactive examples (actual Refast components
rendered alongside their code snippets). Priority:

- [ ] Button variants demo
- [ ] Input + store_as demo
- [ ] Card composition demo
- [ ] Tabs demo
- [ ] Chart demo (one per chart type)
- [ ] Dialog/Sheet/Drawer demo
- [ ] Toast variants demo (with working buttons)

### Search

- [ ] Implement in-page search using `Command*` components (client-side filtering of sidebar items)
