# Advanced Section — Agent Instructions

## Section Goal

Deep-dive topics for **framework extenders and advanced users**. These pages should be
thorough technical references adapted from the existing `.md` docs in the `docs/` folder.

---

## Pages

### 1. `component_dev.py` — Building Components (`/docs/advanced/component-dev`)

**Adapt from:** `docs/COMPONENT_DEVELOPMENT.md` (1938 lines), `docs/NAMING_CONVENTIONS.md`

**Cover:**
- **Architecture overview** — Python class + React component + ComponentRegistry
- **Python side**: Subclass `Component`, implement `render()`, define `component_type`
- **Common props**: id, class_name, children, style, callbacks
- **Children rendering**: `self._render_children()`
- **React side**: Create functional component, register in `ComponentRegistry`
- **Naming conventions**: `snake_case` (Python) → `camelCase` (JSON/React) automatic conversion
- **Callback props**: How `on_click` etc. are serialized and handled
- **Step-by-step walkthrough**: Create a complete custom component from scratch
- **Testing**: How to test custom components

---

### 2. `extension_dev.py` — Building Extensions (`/docs/advanced/extension-dev`)

**Adapt from:** `docs/EXTENSION_DEVELOPMENT.md` (1247 lines)

**Cover:**
- **Extension class**: Subclass `Extension`, define name/version/scripts/styles
- **Project structure**: Python package + static assets
- **Static path**: `@property static_path -> Path`
- **Components**: `@property components -> list` — Python component classes
- **Frontend bundle**: UMD module format, `window.RefastExtensions` / `window.RefastComponentRegistry`
- **Entry points**: `[project.entry-points."refast.extensions"]` in pyproject.toml
- **Auto-discovery**: `auto_discover_extensions=True` on RefastApp
- **Asset serving**: `/static/ext/{name}/{file}` URL pattern
- **on_register()**: Called when extension is registered with app
- **validate()**: Checks static_path exists
- **Building**: How to build the UMD bundle (vite/rollup/webpack)
- **Publishing**: PyPI distribution with entry points
- **Complete example**: Walk through a full extension implementation

---

### 3. `security.py` — Security (`/docs/advanced/security`)

**Read:** All files in `src/refast/security/`

**Cover:**
- **SecurityMiddleware**: Combined middleware (constructor params, processing order)
- **CSRF Protection**: Double-submit cookie, HMAC-SHA256, generate/validate tokens
- **Rate Limiter**: Sliding window, per-key tracking, max_requests/window_seconds
- **Input Sanitizer**: Script tag removal, event handler stripping, javascript: URL blocking
- **Content Security Policy**: CSP header construction, `for_refast()` preset, `for_development()`
- **Configuration examples**: Production vs development setups
- **Decorator usage**: `@csrf_required`, `@rate_limit`, `@sanitize_input`

---

### 4. `sessions.py` — Sessions (`/docs/advanced/sessions`)

**Read:** All files in `src/refast/session/`

**Cover:**
- **Session class**: Dict-like interface, get/set/delete/bracket syntax
- **SessionData**: id, data, created_at, expires_at, modified_at
- **MemoryStore**: In-memory dict (constructor, thread safety, limitations)
- **RedisStore**: Redis-backed (constructor, redis_url, TTL, serialization)
- **SessionMiddleware**: Cookie-based management (constructor params, cookie settings)
- **get_session dependency**: FastAPI dependency injection
- **State vs Session vs Store comparison table** (lifetime, persistence, sharing)
- **Production recommendations**: Redis store, secure cookies, TTL settings

---

### 5. `styling.py` — Styling (`/docs/advanced/styling`)

**Adapt from:** `docs/STYLING_GUIDE.md`, `docs/TAILWIND_SUPPORT.md`

**Cover:**
- **class_name prop**: How every component accepts Tailwind classes
- **Semantic color tokens**: Complete list (background, foreground, primary, secondary, muted, accent, destructive, card, popover, border, input, ring, sidebar, chart-1 through chart-5)
- **Available Tailwind classes**: Layout, spacing (0-6, 8, 10, 12, 16), typography, colors, borders, responsive breakpoints
- **Responsive design**: `sm:`, `md:`, `lg:`, `xl:` prefixes
- **style prop**: When to use it (dynamic values only), examples
- **Custom CSS**: `ui.add_css()`, `custom_css` parameter
- **Custom JS**: `ui.add_js()`, `custom_js` parameter
- **Head tags**: `ui.add_head_tag()` — meta tags, fonts, etc.
- **What's NOT included**: Full Tailwind — only the bundled subset
