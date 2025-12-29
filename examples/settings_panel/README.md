# Settings Panel Example

A multi-section settings interface with sidebar navigation.

## Features Demonstrated

- **Sidebar Navigation** - Section-based navigation with active states
- **Switch** - Boolean toggles for settings
- **Select** - Dropdown selections
- **Input/Textarea** - Text inputs for profile data
- **Avatar** - Profile image display
- **Badge** - Feature labels
- **Card** - Section containers
- **Separator** - Visual dividers

## Sections

1. **Profile** - User information, avatar, bio
2. **Notifications** - Email and push notification preferences
3. **Appearance** - Theme, language, font size
4. **Security** - Password, 2FA, active sessions
5. **Billing** - Subscription, payment methods, history

## Key Patterns

### Section Navigation
```python
async def change_section(ctx: Context):
    section = ctx.event_data.get("section")
    ctx.state.set("active_section", section)
    await ctx.refresh()
```

### Toggle Settings
```python
async def toggle_setting(ctx: Context):
    key = ctx.event_data.get("key")
    current = ctx.state.get(key, False)
    ctx.state.set(key, not current)
```

## Running

```bash
cd examples/settings_panel
uvicorn app:app --reload
```

Then open http://localhost:8000 in your browser.
