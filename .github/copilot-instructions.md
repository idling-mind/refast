# Refast Framework - AI Coding Agent Instructions

> **IMPORTANT**: This file must be kept up-to-date with the current project structure. When making structural changes to the codebase, update this file accordingly.

## Project Overview

**Refast** is a Python + React UI framework that enables building reactive web applications with Python-first development. It uses FastAPI for the backend and React with shadcn/ui for the frontend.

### Core Principles

1. **Explicit over Magic** - Every callback, event, and state change is explicitly defined
2. **Type Safety** - Full type hints and Pydantic validation throughout
3. **Pluggable Architecture** - Can be added to any existing FastAPI app via `include_router`
4. **Component Isolation** - Each component package is independent
5. **Security First** - CSRF, rate limiting, input sanitization built-in

---

## Current Project Structure

```
refast/
├── .github/
│   ├── copilot-instructions.md    # THIS FILE - AI agent instructions
│   ├── workflows/                  # GitHub Actions CI/CD
│   │   ├── test.yml
│   │   ├── lint.yml
│   │   └── docs.yml
│   └── CODEOWNERS
├── plan/                           # Development plans and roadmaps
│   ├── README.md
│   ├── stage-1-core.md
│   ├── stage-2-components.md
│   ├── stage-3-events.md
│   ├── stage-4-sessions.md
│   ├── stage-5-security.md
│   ├── stage-6-frontend.md
│   ├── stage-7-integration.md
│   └── stage-8-docs.md
├── src/
│   └── refast/                     # Main Python package
│       ├── __init__.py
│       ├── app.py                  # RefastApp main class
│       ├── router.py               # FastAPI router integration
│       ├── context.py              # Context class for callbacks
│       ├── state.py                # State management
│       ├── components/
│       │   ├── __init__.py
│       │   ├── base.py             # Base component classes
│       │   ├── registry.py         # Component registry
│       │   ├── slot.py             # Slot component for placeholders
│       │   └── shadcn/             # shadcn-based components
│       │       ├── __init__.py
│       │       ├── button.py
│       │       ├── card.py
│       │       ├── input.py
│       │       ├── form.py
│       │       ├── layout.py
│       │       ├── feedback.py
│       │       └── data_display.py
│       ├── events/
│       │   ├── __init__.py
│       │   ├── manager.py          # Event routing and handling
│       │   ├── stream.py           # WebSocket streaming
│       │   ├── broadcast.py        # Broadcast to all clients
│       │   └── types.py            # Event type definitions
│       ├── session/
│       │   ├── __init__.py
│       │   ├── session.py          # Session management
│       │   ├── stores/
│       │   │   ├── __init__.py
│       │   │   ├── base.py         # Abstract base store
│       │   │   ├── memory.py       # In-memory store
│       │   │   └── redis.py        # Redis store
│       │   └── middleware.py       # Session middleware
│       ├── security/
│       │   ├── __init__.py
│       │   ├── csrf.py             # CSRF protection
│       │   ├── rate_limit.py       # Rate limiting
│       │   ├── sanitizer.py        # Input sanitization
│       │   ├── csp.py              # Content Security Policy
│       │   └── middleware.py       # Security middleware
│       ├── theme/
│       │   ├── __init__.py
│       │   ├── theme.py            # Theme configuration
│       │   └── defaults.py         # Default themes
│       └── updates/
│           ├── __init__.py
│           ├── operations.py       # Update operations enum
│           └── messages.py         # Update message types
├── src/refast-client/              # React frontend package
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── tailwind.config.js          # Tailwind CSS configuration
│   ├── postcss.config.js           # PostCSS configuration
│   ├── src/
│   │   ├── index.tsx               # Entry point (imports CSS)
│   │   ├── index.css               # Tailwind directives + CSS variables
│   │   ├── App.tsx
│   │   ├── components/
│   │   │   ├── ComponentRenderer.tsx
│   │   │   └── shadcn/             # shadcn component wrappers
│   │   ├── events/
│   │   │   ├── EventManager.ts
│   │   │   ├── WebSocketClient.ts
│   │   │   └── types.ts
│   │   ├── session/
│   │   │   └── SessionManager.ts
│   │   ├── state/
│   │   │   └── StateManager.ts
│   │   └── utils/
│   │       └── index.ts
│   └── dist/                       # Built assets (generated)
├── tests/
│   ├── __init__.py
│   ├── conftest.py                 # Pytest fixtures
│   ├── unit/
│   │   ├── test_app.py
│   │   ├── test_components.py
│   │   ├── test_context.py
│   │   ├── test_events.py
│   │   ├── test_session.py
│   │   └── test_security.py
│   ├── integration/
│   │   ├── test_websocket.py
│   │   ├── test_full_flow.py
│   │   └── test_fastapi_integration.py
│   └── e2e/
│       ├── playwright.config.ts
│       └── specs/
│           ├── basic.spec.ts
│           └── events.spec.ts
├── docs/                           # Documentation (built with Refast!)
│   ├── app.py                      # Documentation app
│   ├── pages/
│   │   ├── index.py
│   │   ├── getting_started.py
│   │   ├── components.py
│   │   ├── events.py
│   │   ├── sessions.py
│   │   ├── security.py
│   │   └── api_reference.py
│   └── components/
│       ├── code_block.py
│       ├── api_doc.py
│       └── example.py
├── examples/
│   ├── basic/
│   │   └── app.py
│   ├── todo_app/
│   │   └── app.py
│   ├── chat_app/
│   │   └── app.py
│   └── dashboard/
│       └── app.py
├── pyproject.toml
├── README.md
├── LICENSE
└── CHANGELOG.md
```

---

## AI Agent Guidelines

### Before Starting Any Task

1. **Read the relevant plan file** in `./plan/` for the stage you're working on
2. **Check existing code** to understand current implementations
3. **Review test files** to understand expected behavior
4. **Check this file** for any recent structural changes

### Code Style Requirements

#### Python Code

```python
# Use type hints everywhere
from typing import Any, Callable, TypeVar, Generic

# Use Pydantic for data models
from pydantic import BaseModel, Field

class MyModel(BaseModel):
    """Always include docstrings."""
    name: str = Field(..., description="The name field")
    value: int = Field(default=0, ge=0)

# Use async/await for all I/O operations
async def my_function(param: str) -> dict[str, Any]:
    """
    Brief description.
    
    Args:
        param: Description of param
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When param is invalid
    """
    pass

# Use explicit imports, not star imports
from refast.components import Button, Card, Container  # Good
from refast.components import *  # Bad
```

#### TypeScript/React Code

```typescript
// Use TypeScript strict mode
// Use functional components with hooks
// Use explicit prop types

interface ButtonProps {
  label: string;
  onClick?: () => void;
  variant?: 'primary' | 'secondary' | 'ghost';
}

export function Button({ label, onClick, variant = 'primary' }: ButtonProps) {
  return (
    <button className={`btn-${variant}`} onClick={onClick}>
      {label}
    </button>
  );
}
```

#### Frontend Styling Requirements

> **CRITICAL**: The frontend must be production-ready. No bandaid fixes or workarounds.

1. **Use Tailwind CSS** - All styling must use Tailwind CSS utility classes
2. **Use shadcn/ui patterns** - Follow shadcn/ui component patterns and design tokens
3. **No inline styles** - Never use inline `style` props for styling (except for truly dynamic values like calculated positions)
4. **CSS Variables** - Use CSS custom properties for theming (defined in `src/index.css`)
5. **Bundle CSS** - Tailwind CSS must be properly bundled with the build output

**Frontend Build Output Requirements:**
- `refast-client.js` - IIFE bundle with React and all dependencies included
- `refast-client.css` - Compiled Tailwind CSS with all used classes

**CSS Architecture:**
```
src/refast-client/
├── src/
│   ├── index.css           # Tailwind directives + CSS variables
│   ├── index.tsx           # Must import index.css
│   └── components/
│       └── shadcn/         # Components use Tailwind classes via cn() utility
├── tailwind.config.js      # Tailwind configuration with shadcn theme
├── postcss.config.js       # PostCSS with Tailwind plugin
└── vite.config.ts          # Configured to output separate CSS file
```

**Example Component (Correct):**
```typescript
import { cn } from '../../utils';

export function Button({ variant = 'default', className, ...props }: ButtonProps) {
  return (
    <button
      className={cn(
        'inline-flex items-center justify-center rounded-md font-medium',
        'bg-primary text-primary-foreground hover:bg-primary/90',
        className
      )}
      {...props}
    />
  );
}
```

**Example Component (WRONG - Never do this):**
```typescript
// ❌ WRONG: Inline styles
export function Button({ ...props }: ButtonProps) {
  return (
    <button
      style={{ backgroundColor: '#2563eb', color: 'white' }}
      {...props}
    />
  );
}
```

### Testing Requirements

1. **Unit Tests**: Every function/class must have unit tests
2. **Integration Tests**: Test component interactions and WebSocket flows
3. **E2E Tests**: Use Playwright for browser-based testing
4. **Coverage**: Maintain >80% code coverage

```python
# Test file naming: test_<module>.py
# Test function naming: test_<function>_<scenario>

import pytest
from refast import RefastApp

class TestRefastApp:
    """Group related tests in classes."""
    
    def test_create_app_with_defaults(self):
        """Test description as docstring."""
        app = RefastApp()
        assert app.title == "Refast App"
    
    @pytest.mark.asyncio
    async def test_page_registration(self):
        """Async tests need the marker."""
        app = RefastApp()
        
        @app.page("/")
        def home(ctx):
            return Container()
        
        assert "/" in app.pages
```

### Documentation Requirements

1. **Docstrings**: All public functions, classes, and modules
2. **Type Hints**: Complete type annotations
3. **Examples**: Include usage examples in docstrings
4. **API Docs**: Auto-generated from docstrings
5. **Guides**: Written in the docs app using Refast itself

### When Making Changes

1. **Update tests first** (TDD approach when possible)
2. **Implement the feature**
3. **Run all tests**: `pytest tests/`
4. **Run linting**: `ruff check src/`
5. **Update documentation** if API changes
6. **Update this file** if structure changes

---

## Stage-by-Stage Implementation

See `./plan/` directory for detailed implementation plans:

| Stage | File | Description |
|-------|------|-------------|
| 1 | `stage-1-core.md` | Core framework (App, Router, Context) |
| 2 | `stage-2-components.md` | Component system and base components |
| 3 | `stage-3-events.md` | Event handling and WebSocket |
| 4 | `stage-4-sessions.md` | Session management |
| 5 | `stage-5-security.md` | Security features |
| 6 | `stage-6-frontend.md` | React frontend client |
| 7 | `stage-7-integration.md` | Full integration and examples |
| 8 | `stage-8-docs.md` | Documentation app |

---

## Common Patterns

### Creating a New Component

```python
# src/refast/components/shadcn/my_component.py

from refast.components.base import Component
from refast.events.types import Callback
from typing import Any

class MyComponent(Component):
    """
    Brief description of the component.
    
    Example:
        ```python
        MyComponent(
            title="Hello",
            on_click=ctx.callback(handle_click)
        )
        ```
    
    Args:
        title: The title to display
        on_click: Optional click callback
    """
    
    component_type: str = "MyComponent"
    
    def __init__(
        self,
        title: str,
        on_click: Callback | None = None,
        id: str | None = None,
        class_name: str = "",
        **props: Any,
    ):
        super().__init__(id=id, class_name=class_name)
        self.title = title
        self.on_click = on_click
        self.props = props
    
    def render(self) -> dict[str, Any]:
        return {
            "type": self.component_type,
            "id": self.id,
            "props": {
                "title": self.title,
                "className": self.class_name,
                "onClick": self.on_click.serialize() if self.on_click else None,
                **self.props,
            },
            "children": self._render_children(),
        }
```

### Creating a New Event Handler

```python
# In the app definition

@ui.on_event("my:event")
async def handle_my_event(ctx: Context, event: Event):
    """
    Handle the my:event event.
    
    Args:
        ctx: The request context
        event: The event data
    """
    # Process event
    result = await process_event(event.data)
    
    # Push update to client
    await ctx.push_event("my:result", result)
```

### Adding a New Session Store

```python
# src/refast/session/stores/my_store.py

from refast.session.stores.base import SessionStore
from typing import Any

class MyStore(SessionStore):
    """Custom session store implementation."""
    
    async def get(self, session_id: str) -> dict[str, Any] | None:
        """Retrieve session data."""
        pass
    
    async def set(self, session_id: str, data: dict[str, Any], ttl: int) -> None:
        """Store session data."""
        pass
    
    async def delete(self, session_id: str) -> None:
        """Delete session data."""
        pass
    
    async def exists(self, session_id: str) -> bool:
        """Check if session exists."""
        pass
```

---

## Updating This File

When the project structure changes:

1. Update the "Current Project Structure" section
2. Update any affected patterns or examples
3. Update the stage plan files if needed
4. Commit with message: `docs: update copilot instructions for [change]`

### Structure Change Checklist

- [ ] Updated directory tree in this file
- [ ] Updated relevant plan stage file
- [ ] Updated examples if affected
- [ ] Updated test structure if affected
- [ ] Added migration notes if breaking change

---

## Environment Setup

Before running any commands, ensure uv is in your PATH:

```powershell
$env:PATH = "t:\cae\ETT\pygkn-uv\;" + $env:PATH
```

Then create and activate the virtual environment:

```bash
# Create virtual environment
uv venv

# Install with dev dependencies
uv pip install -e ".[dev]"
```

---

## Quick Reference

### Running Tests

```bash
# All tests (using uv)
uv run pytest tests/ tests/

# Specific stage
uv run pytest tests/unit/test_app.py

# With coverage
uv run pytest tests/ --cov=src/refast --cov-report=html

# E2E tests
cd src/refast-client && npx playwright test
```

### Running Linting

```bash
# Python (using uv)
uv run ruff check src/
uv run ruff format src/

# TypeScript
cd src/refast-client && npm run lint
```

### Building

```bash
# Python package
python -m build

# Frontend
cd src/refast-client && npm run build
```

### Running Documentation

```bash
cd docs && uvicorn app:app --reload
```

---

## Current Implementation Status

<!-- This section should be updated as stages are completed -->

| Stage | Status | Notes |
|-------|--------|-------|
| 1 - Core | 🟢 Complete | RefastApp, Router, Context, State implemented with 74 tests |
| 2 - Components | 🟢 Complete | Base, Registry, Slot, Layout, Input, Form, Feedback, Data Display, Typography - 154 tests |
| 3 - Events | 🟢 Complete | Event types, EventManager, WebSocket stream, BroadcastManager - 79 tests |
| 4 - Sessions | 🟢 Complete | Session, SessionData, MemoryStore, RedisStore, SessionMiddleware - 58 tests |
| 5 - Security | 🟢 Complete | CSRFProtection, RateLimiter, InputSanitizer, ContentSecurityPolicy, SecurityMiddleware - 125 tests |
| 6 - Frontend | 🟢 Complete | React client with ComponentRenderer, EventManager, WebSocket, StateManager, shadcn components - 60 tests |
| 7 - Integration | 🟢 Complete | Integration tests (26), asset bundling, 4 example apps (basic, todo, chat, dashboard), E2E test setup - 516 total tests |
| 8 - Documentation | 🔴 Not Started | |

Legend: 🔴 Not Started | 🟡 In Progress | 🟢 Complete

---

## Contact and Resources

- **Repository**: [GitHub URL]
- **Documentation**: Built with Refast (see `/docs`)
- **Examples**: See `/examples` directory
