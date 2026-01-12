"""
JavaScript Callbacks Example

This example demonstrates how to use ctx.js() and ctx.call_js() to execute
JavaScript directly in the browser without a server roundtrip.

Features demonstrated:
- ctx.js() for event handlers (on_click, on_change)
- ctx.call_js() for executing JS from Python callbacks
- Bound arguments in JavaScript callbacks
- Accessing event data in JavaScript
- Combining JavaScript and Python callbacks

Run with:
    cd examples/js_callbacks
    uvicorn app:app --reload
"""

from textwrap import dedent
from fastapi import FastAPI

from refast import Context, RefastApp
from refast.components import (
    Badge,
    Button,
    Card,
    CardContent,
    CardDescription,
    CardHeader,
    CardTitle,
    Column,
    Container,
    Heading,
    Input,
    Row,
    Separator,
    Text,
    Markdown,
    Code,
)

ui = RefastApp(title="JavaScript Callbacks Demo")


# ============================================================================
# Python Callbacks (for comparison)
# ============================================================================


async def python_increment(ctx: Context):
    """Traditional Python callback - requires server roundtrip."""
    count = ctx.state.get("python_count", 0) + 1
    ctx.state.set("python_count", count)
    await ctx.refresh()


async def save_and_celebrate(ctx: Context):
    """
    Demonstrates ctx.call_js() - execute JavaScript after Python logic.
    """
    # Simulate saving to database
    import asyncio

    await asyncio.sleep(0.5)

    # Update state
    save_count = ctx.state.get("save_count", 0) + 1
    ctx.state.set("save_count", save_count)
    await ctx.refresh()

    # Execute JavaScript on the client after save completes
    await ctx.call_js(
        """
        // Create a simple celebration effect
        const celebration = document.createElement('div');
        celebration.innerHTML = '🎉';
        celebration.style.cssText = `
            position: fixed;
            top: 50%;
            left: 50%;
            font-size: 100px;
            transform: translate(-50%, -50%);
            animation: pop 0.5s ease-out forwards;
            pointer-events: none;
            z-index: 9999;
        `;
        
        // Add animation keyframes if not exists
        if (!document.getElementById('celebration-style')) {
            const style = document.createElement('style');
            style.id = 'celebration-style';
            style.textContent = `
                @keyframes pop {
                    0% { transform: translate(-50%, -50%) scale(0); opacity: 1; }
                    100% { transform: translate(-50%, -50%) scale(2); opacity: 0; }
                }
            `;
            document.head.appendChild(style);
        }
        
        document.body.appendChild(celebration);
        setTimeout(() => celebration.remove(), 500);
        
        console.log('Saved ' + args.count + ' times!');
        """,
        count=save_count,
    )

    await ctx.show_toast(f"Saved successfully! (#{save_count})", variant="success")


async def focus_input(ctx: Context):
    """Use ctx.call_js() to focus an input element."""
    await ctx.call_js(
        """
        const input = document.getElementById(args.inputId);
        if (input) {
            input.focus();
            input.select();
        }
        """,
        inputId="focus-target",
    )


# ============================================================================
# State & Store Callbacks
# ============================================================================

# Key prefix used by Refast for localStorage
STORE_PREFIX = "refast:local:"


async def python_set_state_counter(ctx: Context):
    """Set state counter from Python."""
    count = ctx.state.get("state_counter", 0) + 1
    ctx.state.set("state_counter", count)
    await ctx.refresh()


async def python_set_store_counter(ctx: Context):
    """Set localStorage counter from Python - also readable by JS."""
    count = ctx.store.local.get("shared_counter", 0) + 1
    ctx.store.local.set("shared_counter", count)
    await ctx.refresh()


async def python_read_store_value(ctx: Context):
    """
    Read localStorage value that may have been set by JavaScript.
    
    Using await ctx.store.sync() refreshes the cache from the browser,
    so get() will return the latest value including JS changes.
    """
    # Sync store from browser to get JS-modified values
    await ctx.store.sync()
    
    shared_counter = ctx.store.local.get("shared_counter", 0)
    await ctx.show_toast(
        f"Shared counter: {shared_counter}",
        variant="success",
        description="This is the live value from browser localStorage!",
    )


async def js_sync_store_value(ctx: Context):
    """
    Receive a store value from JavaScript and update Python's cache.
    This is the recommended pattern for real-time JS → Python sync.
    """
    # Get the value sent from JavaScript
    new_value = ctx.event_data.get("value", 0)
    
    # Update Python's store cache
    ctx.store.local.set("shared_counter", new_value)
    
    await ctx.show_toast(
        f"Synced from JS: {new_value}",
        variant="success",
        description="Python now has the latest value from JavaScript!",
    )
    
    # Refresh to show updated value
    await ctx.refresh()


# ============================================================================
# Page Definition
# ============================================================================


@ui.page("/")
def home(ctx: Context):
    python_count = ctx.state.get("python_count", 0)
    save_count = ctx.state.get("save_count", 0)

    # State and Store values for Section 8
    state_counter = ctx.state.get("state_counter", 0)
    # Shared counter - can be set by both Python and JavaScript
    shared_counter = ctx.store.local.get("shared_counter", 0)

    return Container(
        class_name="max-w-4xl mx-auto py-8 space-y-8",
        children=[
            # Header
            Column(
                gap=2,
                children=[
                    Heading("JavaScript Callbacks in Refast", level=1),
                    Text(
                        "Learn how to use ctx.js() and ctx.call_js() for client-side JavaScript execution.",
                        class_name="text-muted-foreground text-lg",
                    ),
                ],
            ),
            Separator(),
            # Section 1: Basic JavaScript Callbacks
            Card(
                class_name="mt-4",
                children=[
                    CardHeader(
                        children=[
                            CardTitle("1. Basic ctx.js() Examples"),
                            CardDescription(
                                "Execute JavaScript directly in the browser - no server roundtrip!"
                            ),
                        ]
                    ),
                    CardContent(
                        children=[
                            Column(
                                gap=4,
                                children=[
                                    # Simple alert
                                    Row(
                                        gap=4,
                                        align="center",
                                        children=[
                                            Button(
                                                "Show Alert",
                                                on_click=ctx.js("alert('Hello from JavaScript!')"),
                                            ),
                                            Text(
                                                "→ Uses ctx.js() with simple alert",
                                                class_name="text-sm text-muted-foreground",
                                            ),
                                        ],
                                    ),
                                    # Console log
                                    Row(
                                        gap=4,
                                        align="center",
                                        children=[
                                            Button(
                                                "Log to Console",
                                                variant="outline",
                                                on_click=ctx.js(
                                                    "console.log('Button clicked at:', new Date().toISOString())"
                                                ),
                                            ),
                                            Text(
                                                "→ Open DevTools to see the log",
                                                class_name="text-sm text-muted-foreground",
                                            ),
                                        ],
                                    ),
                                    # Toggle class
                                    Row(
                                        gap=4,
                                        align="center",
                                        children=[
                                            Button(
                                                "Toggle Dark Mode",
                                                variant="secondary",
                                                on_click=ctx.js(
                                                    "document.documentElement.classList.toggle('dark')"
                                                ),
                                            ),
                                            Text(
                                                "→ Toggles dark mode instantly",
                                                class_name="text-sm text-muted-foreground",
                                            ),
                                        ],
                                    ),
                                ],
                            )
                        ]
                    ),
                ]
            ),
            # Section 2: Bound Arguments
            Card(
                class_name="mt-4",
                children=[
                    CardHeader(
                        children=[
                            CardTitle("2. Bound Arguments"),
                            CardDescription(
                                "Pass data from Python to JavaScript using bound arguments."
                            ),
                        ]
                    ),
                    CardContent(
                        children=[
                            Column(
                                gap=4,
                                children=[
                                    Row(
                                        gap=2,
                                        children=[
                                            Button(
                                                "Greet Alice",
                                                on_click=ctx.js(
                                                    "alert('Hello, ' + args.name + '!')",
                                                    name="Alice",
                                                ),
                                            ),
                                            Button(
                                                "Greet Bob",
                                                variant="outline",
                                                on_click=ctx.js(
                                                    "alert('Hello, ' + args.name + '!')",
                                                    name="Bob",
                                                ),
                                            ),
                                            Button(
                                                "Greet Charlie",
                                                variant="secondary",
                                                on_click=ctx.js(
                                                    "alert('Hello, ' + args.name + '!')",
                                                    name="Charlie",
                                                ),
                                            ),
                                        ],
                                    ),
                                    Text(
                                        "Same JS code, different bound arguments",
                                        class_name="text-sm text-muted-foreground",
                                    ),
                                    Separator(),
                                    # Complex data
                                    Button(
                                        "Show User Data",
                                        on_click=ctx.js(
                                            """
                                            const user = args.user;
                                            alert(
                                                'User: ' + user.name + '\\n' +
                                                'Email: ' + user.email + '\\n' +
                                                'Role: ' + user.role
                                            );
                                            """,
                                            user={
                                                "name": "John Doe",
                                                "email": "john@example.com",
                                                "role": "Admin",
                                            },
                                        ),
                                    ),
                                    Text(
                                        "Complex objects can be passed as bound arguments",
                                        class_name="text-sm text-muted-foreground",
                                    ),
                                ],
                            )
                        ]
                    ),
                ]
            ),
            # Section 3: Event Data Access
            Card(
                class_name="mt-4",
                children=[
                    CardHeader(
                        children=[
                            CardTitle("3. Accessing Event Data"),
                            CardDescription(
                                "Use 'event' object to access input values and other event data."
                            ),
                        ]
                    ),
                    CardContent(
                        children=[
                            Column(
                                gap=4,
                                children=[
                                    Input(
                                        name="live-input",
                                        placeholder="Type something and check the console...",
                                        on_change=ctx.js(
                                            "console.log('Input value:', event.value)"
                                        ),
                                    ),
                                    Text(
                                        "→ Open DevTools console to see live input values",
                                        class_name="text-sm text-muted-foreground",
                                    ),
                                    Separator(),
                                    Input(
                                        name="char-count-input",
                                        placeholder="Type here to see character count...",
                                        on_change=ctx.js(
                                            """
                                            const count = (event.value || '').length;
                                            const display = document.getElementById('char-count');
                                            if (display) {
                                                display.textContent = count + ' characters';
                                                display.style.color = count > 20 ? 'red' : 'green';
                                            }
                                            """
                                        ),
                                    ),
                                    Text(
                                        "0 characters",
                                        id="char-count",
                                        class_name="text-sm font-mono",
                                    ),
                                ],
                            )
                        ]
                    ),
                ]
            ),
            # Section 4: Python vs JavaScript Comparison
            Card(
                class_name="mt-4",
                children=[
                    CardHeader(
                        children=[
                            CardTitle("4. Python vs JavaScript Callbacks"),
                            CardDescription(
                                "Compare server-side Python callbacks with client-side JavaScript."
                            ),
                        ]
                    ),
                    CardContent(
                        children=[
                            Row(
                                gap=8,
                                children=[
                                    # Python callback column
                                    Column(
                                        gap=2,
                                        class_name="flex-1",
                                        children=[
                                            Text("Python Callback", class_name="font-semibold"),
                                            Text(
                                                "Requires WebSocket roundtrip",
                                                class_name="text-sm text-muted-foreground",
                                            ),
                                            Button(
                                                f"Count: {python_count}",
                                                id="python-counter-button",
                                                on_click=ctx.callback(python_increment),
                                                class_name="w-full",
                                            ),
                                            Badge(
                                                "Server-side",
                                                variant="secondary",
                                            ),
                                        ],
                                    ),
                                    # JavaScript callback column
                                    Column(
                                        gap=2,
                                        class_name="flex-1",
                                        children=[
                                            Text("JavaScript Callback", class_name="font-semibold"),
                                            Text(
                                                "Instant, no server roundtrip",
                                                class_name="text-sm text-muted-foreground",
                                            ),
                                            Button(
                                                "Instant Counter",
                                                variant="outline",
                                                on_click=ctx.js(
                                                    """
                                                    const btn = element;
                                                    let count = parseInt(btn.dataset.count || '0') + 1;
                                                    btn.dataset.count = count;
                                                    btn.textContent = 'Count: ' + count;
                                                    """
                                                ),
                                                class_name="w-full",
                                            ),
                                            Badge(
                                                "Client-side",
                                                variant="default",
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                            Text(
                                "Note: JavaScript counter resets on page refresh. "
                                "Python counter persists in state.",
                                class_name="text-sm text-muted-foreground mt-4",
                            ),
                        ]
                    ),
                ]
            ),
            # Section 5: ctx.call_js() from Python
            Card(
                class_name="mt-4",
                children=[
                    CardHeader(
                        children=[
                            CardTitle("5. ctx.call_js() - Execute JS from Python"),
                            CardDescription(
                                "Run JavaScript after server-side logic completes."
                            ),
                        ]
                    ),
                    CardContent(
                        children=[
                            Column(
                                gap=4,
                                children=[
                                    Row(
                                        gap=4,
                                        children=[
                                            Button(
                                                f"Save & Celebrate ({save_count})",
                                                on_click=ctx.callback(save_and_celebrate),
                                            ),
                                            Button(
                                                "Focus Input Below",
                                                variant="outline",
                                                on_click=ctx.callback(focus_input),
                                            ),
                                        ],
                                    ),
                                    Input(
                                        id="focus-target",
                                        name="focus-target",
                                        placeholder="This input will be focused...",
                                    ),
                                    Text(
                                        "→ 'Save & Celebrate' simulates a save operation, "
                                        "then triggers a celebration animation via ctx.call_js()",
                                        class_name="text-sm text-muted-foreground",
                                    ),
                                ],
                            )
                        ]
                    ),
                ]
            ),
            # Section 6: DOM Manipulation
            Card(
                class_name="mt-4",
                children=[
                    CardHeader(
                        children=[
                            CardTitle("6. DOM Manipulation"),
                            CardDescription(
                                "Directly manipulate the DOM with JavaScript callbacks."
                            ),
                        ]
                    ),
                    CardContent(
                        children=[
                            Column(
                                gap=4,
                                children=[
                                    Row(
                                        gap=2,
                                        children=[
                                            Button(
                                                "Scroll to Top",
                                                variant="outline",
                                                on_click=ctx.js(
                                                    "window.scrollTo({ top: 0, behavior: 'smooth' })"
                                                ),
                                            ),
                                            Button(
                                                "Scroll to Bottom",
                                                variant="outline",
                                                on_click=ctx.js(
                                                    "window.scrollTo({ top: document.body.scrollHeight, behavior: 'smooth' })"
                                                ),
                                            ),
                                        ],
                                    ),
                                    Separator(),
                                    Row(
                                        gap=2,
                                        children=[
                                            Button(
                                                "Add Box",
                                                on_click=ctx.js(
                                                    """
                                                    const container = document.getElementById('box-container');
                                                    if (container) {
                                                        const box = document.createElement('div');
                                                        box.className = 'w-8 h-8 bg-primary rounded animate-pulse';
                                                        box.style.animationDelay = (container.children.length * 0.1) + 's';
                                                        container.appendChild(box);
                                                    }
                                                    """
                                                ),
                                            ),
                                            Button(
                                                "Clear Boxes",
                                                variant="destructive",
                                                on_click=ctx.js(
                                                    """
                                                    const container = document.getElementById('box-container');
                                                    if (container) container.innerHTML = '';
                                                    """
                                                ),
                                            ),
                                        ],
                                    ),
                                    Row(
                                        id="box-container",
                                        gap=2,
                                        class_name="min-h-12 p-2 border rounded flex-wrap",
                                    ),
                                ],
                            )
                        ]
                    ),
                ]
            ),
            # Section 7: Clipboard & Browser APIs
            Card(
                class_name="mt-4",
                children=[
                    CardHeader(
                        children=[
                            CardTitle("7. Browser APIs"),
                            CardDescription(
                                "Access browser APIs like Clipboard, Notifications, and more."
                            ),
                        ]
                    ),
                    CardContent(
                        children=[
                            Column(
                                gap=4,
                                children=[
                                    Row(
                                        gap=2,
                                        children=[
                                            Button(
                                                "Copy to Clipboard",
                                                on_click=ctx.js(
                                                    """
                                                    navigator.clipboard.writeText(args.text).then(() => {
                                                        alert('Copied: ' + args.text);
                                                    }).catch(err => {
                                                        alert('Failed to copy: ' + err);
                                                    });
                                                    """,
                                                    text="Hello from Refast! 🚀",
                                                ),
                                            ),
                                            Button(
                                                "Get Current Time",
                                                variant="outline",
                                                on_click=ctx.js(
                                                    """
                                                    const now = new Date();
                                                    const timeStr = now.toLocaleTimeString();
                                                    document.getElementById('time-display').textContent = timeStr;
                                                    """
                                                ),
                                            ),
                                        ],
                                    ),
                                    Text(
                                        "Current time: --:--:--",
                                        id="time-display",
                                        class_name="font-mono",
                                    ),
                                    Separator(),
                                    Button(
                                        "Request Notification Permission",
                                        variant="secondary",
                                        on_click=ctx.js(
                                            """
                                            if ('Notification' in window) {
                                                Notification.requestPermission().then(permission => {
                                                    if (permission === 'granted') {
                                                        new Notification('Refast', {
                                                            body: 'Notifications enabled!',
                                                            icon: '🔔'
                                                        });
                                                    } else {
                                                        alert('Notification permission: ' + permission);
                                                    }
                                                });
                                            } else {
                                                alert('Notifications not supported');
                                            }
                                            """
                                        ),
                                    ),
                                ],
                            )
                        ]
                    ),
                ]
            ),
            # Section 8: State & Store - Python vs JavaScript
            Card(
                class_name="mt-4",
                children=[
                    CardHeader(
                        children=[
                            CardTitle("8. State & Store: Python vs JavaScript"),
                            CardDescription(
                                "Compare updating state and localStorage from Python and JavaScript."
                            ),
                        ]
                    ),
                    CardContent(
                        children=[
                            Column(
                                gap=6,
                                children=[
                                    # Subsection: Python State
                                    Column(
                                        gap=2,
                                        children=[
                                            Text("Python State (ctx.state)", class_name="font-semibold text-lg"),
                                            Text(
                                                "State managed by Python - persists during session, syncs to frontend on refresh.",
                                                class_name="text-sm text-muted-foreground",
                                            ),
                                            Row(
                                                gap=4,
                                                align="center",
                                                children=[
                                                    Button(
                                                        f"Python State: {state_counter}",
                                                        on_click=ctx.callback(python_set_state_counter),
                                                    ),
                                                    Badge("Server roundtrip", variant="secondary"),
                                                ],
                                            ),
                                        ],
                                    ),
                                    Separator(),
                                    # Subsection: JavaScript DOM State
                                    Column(
                                        gap=2,
                                        children=[
                                            Text("JavaScript DOM State", class_name="font-semibold text-lg"),
                                            Text(
                                                "State stored in DOM - instant updates, but NOT synced to Python.",
                                                class_name="text-sm text-muted-foreground",
                                            ),
                                            Row(
                                                gap=4,
                                                align="center",
                                                children=[
                                                    Button(
                                                        "JS State: 0",
                                                        id="js-state-display",
                                                        variant="outline",
                                                        on_click=ctx.js(
                                                            """
                                                            const btn = element;
                                                            let count = parseInt(btn.dataset.count || '0') + 1;
                                                            btn.dataset.count = count;
                                                            btn.textContent = 'JS State: ' + count;
                                                            """
                                                        ),
                                                    ),
                                                    Badge("No server roundtrip", variant="default"),
                                                ],
                                            ),
                                            Text(
                                                "⚠️ This value resets on page refresh and Python cannot read it.",
                                                class_name="text-sm text-yellow-600 dark:text-yellow-400",
                                            ),
                                        ],
                                    ),
                                    Separator(),
                                    # Subsection: Python Store (localStorage)
                                    Column(
                                        gap=2,
                                        children=[
                                            Text("Shared Store (localStorage)", class_name="font-semibold text-lg"),
                                            Text(
                                                "localStorage can be read and written by BOTH Python and JavaScript!",
                                                class_name="text-sm text-muted-foreground",
                                            ),
                                            Text(
                                                f"Key: 'refast:local:shared_counter' — Python uses ctx.store.local, JS must use the prefixed key.",
                                                class_name="text-xs font-mono text-muted-foreground",
                                            ),
                                            Row(
                                                gap=4,
                                                align="center",
                                                children=[
                                                    Button(
                                                        f"Python Set: {shared_counter}",
                                                        on_click=ctx.callback(python_set_store_counter),
                                                    ),
                                                    Button(
                                                        "JS Increment",
                                                        variant="outline",
                                                        on_click=ctx.js(
                                                            """
                                                            // Read current value using the refast prefix
                                                            const key = 'refast:local:shared_counter';
                                                            let current = parseInt(localStorage.getItem(key) || '0');
                                                            current += 1;
                                                            localStorage.setItem(key, current.toString());
                                                            
                                                            // Update display
                                                            const display = document.getElementById('shared-counter-display');
                                                            if (display) display.textContent = current;
                                                            
                                                            console.log('JS set shared_counter to:', current);
                                                            """
                                                        ),
                                                    ),
                                                    Button(
                                                        "Read in Python",
                                                        variant="secondary",
                                                        on_click=ctx.callback(python_read_store_value),
                                                    ),
                                                ],
                                            ),
                                            Row(
                                                gap=2,
                                                align="center",
                                                children=[
                                                    Text("Current value:", class_name="text-sm"),
                                                    Text(
                                                        str(shared_counter),
                                                        id="shared-counter-display",
                                                        class_name="text-lg font-bold font-mono bg-muted px-3 py-1 rounded",
                                                    ),
                                                ],
                                            ),
                                            Text(
                                                "✅ Both Python and JS can read/write. Store auto-syncs from browser before each callback!",
                                                class_name="text-sm text-green-600 dark:text-green-400",
                                            ),
                                        ],
                                    ),
                                    Separator(),
                                    # Subsection: How to share values
                                    Column(
                                        gap=2,
                                        children=[
                                            Text("How It Works", class_name="font-semibold text-lg"),
                                            Code(
                                                code=dedent("""
                                                    # Python - set/get values"),
                                                    ctx.store.local.set('shared_counter', 42)
                                                    value = ctx.store.local.get('shared_counter')
                                                    
                                                    # To read JS-modified values, sync first:
                                                    await ctx.store.sync()
                                                    value = ctx.store.local.get('js_set_key')

                                                    // JavaScript - must use 'refast:local:' prefix
                                                    localStorage.setItem('refast:local:shared_counter', '42')
                                                    let val = localStorage.getItem('refast:local:shared_counter')
                                                    """
                                                ),
                                                language="python",
                                                inline=False
                                            ),
                                        ],
                                    ),
                                    Separator(),
                                    # Summary table
                                    Column(
                                        gap=2,
                                        children=[
                                            Text("Summary", class_name="font-semibold"),
                                            Markdown(
                                                """
| Method                   | Instant  | Persists  | Py Reads        | JS Reads   |
|--------------------------|----------|-----------|-----------------|-------------|
| ctx.state                | No       | Session   | ✅ Yes          | ❌ No      |
| ctx.store.local          | No       | Forever   | ✅ Yes          | ✅ Yes*    |
| JS DOM state             | ✅ Yes  | No        | ❌ No           | ✅ Yes     |
| JS localStorage (prefix) | ✅ Yes   | Forever   | ✅ With sync**  | ✅ Yes     |

*  JS reads via: `localStorage.getItem('refast:local:key')`
* Use `await ctx.store.sync()` to refresh cache from browser
                                                """,
                                                class_name="prose-sm"
                                            ),
                                        ],
                                    ),
                                ],
                            )
                        ]
                    ),
                ]
            ),
            # Footer
            Separator(),
            Text(
                "💡 Tip: Open your browser's DevTools (F12) to see console.log outputs!",
                class_name="text-center text-muted-foreground",
            ),
        ],
    )


# Create FastAPI app
app = FastAPI()
app.include_router(ui.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
