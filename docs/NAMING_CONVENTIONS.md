# Naming Conventions in Refast

This document describes the naming conventions used in Refast for props, events, and data transfer between the Python backend and React frontend.

## Overview

Refast bridges two ecosystems with different naming conventions:

| Layer | Convention | Example |
|-------|------------|---------|
| **Python (Backend)** | snake_case | `on_click`, `class_name`, `max_value` |
| **TypeScript (Frontend)** | camelCase | `onClick`, `className`, `maxValue` |

**Key Principle**: The conversion boundary is at the frontend's `ComponentRenderer`, which automatically converts snake_case props to camelCase.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Python Backend                               │
│                                                                       │
│   Component.render() → { "props": { "on_click": ..., "max_value": 5 } }   │
│                              ↓                                        │
│                         snake_case                                    │
└─────────────────────────────────────────────────────────────────────┘
                               ↓ WebSocket/JSON
┌─────────────────────────────────────────────────────────────────────┐
│                       React Frontend                                  │
│                                                                       │
│   ComponentRenderer.tsx:                                              │
│   - Receives: { "on_click": ..., "max_value": 5 }                    │
│   - Converts: snakeToCamel(key) for each prop                        │
│   - Passes:   { onClick: ..., maxValue: 5 } to React component       │
│                                                                       │
│   React Component receives camelCase props as expected               │
└─────────────────────────────────────────────────────────────────────┘
```

## Rules

### 1. Python Component Props → Use snake_case

All prop keys emitted from Python `render()` methods **MUST** use snake_case:

```python
# ✅ CORRECT
def render(self) -> dict[str, Any]:
    return {
        "type": self.component_type,
        "id": self.id,
        "props": {
            "class_name": self.class_name,      # NOT className
            "on_click": self.on_click.serialize() if self.on_click else None,
            "max_value": self.max_value,        # NOT maxValue
            "is_disabled": self.disabled,       # NOT isDisabled
            "icon_position": self.icon_position, # NOT iconPosition
        },
        "children": self._render_children(),
    }

# ❌ WRONG - camelCase props will NOT be converted
def render(self) -> dict[str, Any]:
    return {
        "props": {
            "className": self.class_name,    # WRONG - won't work!
            "onClick": self.on_click,        # WRONG
            "maxValue": self.max_value,      # WRONG
        }
    }
```

### 2. Python API Methods → Use snake_case

All Python method parameters use snake_case:

```python
# ✅ CORRECT
await ctx.update_props("my-id", {"foreground_color": "red"})
await ctx.show_toast("Hello", close_button=True, toast_id="msg-1")

# ❌ WRONG
await ctx.update_props("my-id", {"foregroundColor": "red"})
await ctx.show_toast("Hello", closeButton=True, toastId="msg-1")
```

### 3. Internal Wire Format → camelCase

Internal serialization fields (not user-facing props) use camelCase for efficiency since they're consumed directly by TypeScript:

```python
# Callback serialization (internal)
{
    "callbackId": "uuid-string",  # camelCase - consumed by JS directly
    "boundArgs": {...},
    "debounce": 300,
}

# Event serialization (internal)
{
    "sessionId": "...",    # camelCase
    "eventId": "...",      # camelCase
}

# WebSocket messages (internal)
{
    "type": "update",
    "targetId": "component-id",  # camelCase
    "operation": "replace",
}
```

**Rationale**: These fields are internal protocol fields, not component props. They're processed by framework code on both sides and don't go through `ComponentRenderer`'s prop conversion.

### 4. React Component Props → Receive camelCase

Frontend React components receive props already converted to camelCase:

```typescript
// The component receives camelCase props
interface ButtonProps {
  onClick?: () => void;     // Converted from on_click
  className?: string;        // Converted from class_name  
  iconPosition?: 'left' | 'right';  // Converted from icon_position
  maxValue?: number;         // Converted from max_value
}

export function Button({ onClick, className, iconPosition }: ButtonProps) {
  // ... component implementation
}
```

## Conversion Functions

### Frontend (TypeScript)

Located in `ComponentRenderer.tsx`:

```typescript
function snakeToCamel(str: string): string {
  return str.replace(/_([a-z])/g, (_, letter) => letter.toUpperCase());
}
// "on_click" → "onClick"
// "max_value" → "maxValue"
```

### Backend (Python)

Located in `src/refast/utils/case.py`:

```python
from refast.utils import snake_to_camel, camel_to_snake

snake_to_camel("on_click")  # → "onClick"
camel_to_snake("onClick")    # → "on_click"

# For converting entire dictionaries
from refast.utils import convert_keys_to_camel, convert_keys_to_snake

convert_keys_to_camel({"my_key": "value"})  # → {"myKey": "value"}
convert_keys_to_snake({"myKey": "value"})   # → {"my_key": "value"}
```

## Development Validation

Enable prop validation to catch camelCase props during development:

```bash
# Set environment variable
export REFAST_VALIDATE_PROPS=1  # Linux/Mac
set REFAST_VALIDATE_PROPS=1     # Windows CMD
$env:REFAST_VALIDATE_PROPS="1"  # PowerShell
```

This will log warnings when components emit camelCase prop keys:

```
WARNING - [Button] Props contain camelCase keys which should be snake_case: 
['iconPosition']. The frontend will NOT convert these correctly.
Use snake_case (e.g., 'icon_position' instead of 'iconPosition').
```

You can also manually validate props in your component:

```python
def render(self) -> dict[str, Any]:
    props = {
        "value": self.value,
        "on_change": self.on_change.serialize() if self.on_change else None,
    }
    self._validate_props(props)  # Logs warning if camelCase found
    return {
        "type": self.component_type,
        "id": self.id,
        "props": props,
        "children": [],
    }
```

## Edge Cases

### Leading Underscores

Leading underscores are preserved:

```python
"_private_prop" → "_privateProp"
```

### Consecutive Underscores

Consecutive underscores are collapsed:

```python
"some__value" → "someValue"
```

### Already camelCase

Props that are already camelCase pass through unchanged (but this is incorrect usage):

```python
"onClick" → "onClick"  # Passes through, but DON'T DO THIS
```

### Acronyms

Acronyms are lowercased after the first letter:

```python
"html_id" → "htmlId"   # NOT htmlID
"get_http_response" → "getHttpResponse"
```

## Summary Table

| Context | Convention | Example | Notes |
|---------|------------|---------|-------|
| Python prop keys | snake_case | `on_click` | Converted by frontend |
| Python method args | snake_case | `ctx.show_toast(close_button=True)` | Standard Python |
| TypeScript props | camelCase | `onClick` | Standard React |
| Callback serialization | camelCase | `callbackId` | Internal protocol |
| WebSocket messages | camelCase | `targetId` | Internal protocol |
| Event data keys | camelCase | `sessionId` | Internal protocol |

## Migration Guide

If you have existing components using camelCase props:

1. Enable validation: `REFAST_VALIDATE_PROPS=1`
2. Run your app and check logs for warnings
3. Update Python `render()` methods to use snake_case
4. The frontend automatically handles the conversion

**Before:**
```python
props["iconPosition"] = self.icon_position  # ❌ camelCase
```

**After:**
```python
props["icon_position"] = self.icon_position  # ✅ snake_case
```

No frontend changes needed—`ComponentRenderer` handles the conversion automatically.
