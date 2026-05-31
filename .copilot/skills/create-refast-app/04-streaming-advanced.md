# Refast — Streaming, Long-Running Tasks & Realtime

## 1. Streaming Text Output (LLM Pattern)

Use `ctx.append_prop(id, prop, value)` to incrementally push content to a component already rendered in the browser.

### Components that support streaming

- `rc.Markdown(id="output", content="")` — streams Markdown/text
- `rc.Text(id="output", children="")` — streams plain text
- Custom chart components — stream data points via `data` prop

### Token-by-Token Streaming

```python
@ui.page("/")
def page(ctx: Context):
    return rc.Column(children=[
        rc.Row(children=[
            rc.Button("Stream", on_click=ctx.callback(start_stream)),
            rc.Button("Stop", on_click=ctx.callback(stop_stream)),
        ]),
        rc.ScrollArea(
            id="scroll-area",
            style={"height": "400px"},
            stick_to_bottom=True,          # auto-scrolls to new content
            children=[
                rc.Markdown(id="output", content=""),
            ],
        ),
        rc.Text(id="status", children="Idle"),
    ])

async def start_stream(ctx: Context):
    # 1. Reset output and show streaming indicator
    await ctx.update_props("output", {"content": "", "streaming": True})
    await ctx.update_text("status", "Streaming...")
    ctx.state.set("streaming_active", True)

    # 2. Stream tokens
    async for chunk in my_llm_stream(prompt):
        if not ctx.state.get("streaming_active", True):
            break
        await ctx.append_prop("output", "content", chunk)

    # 3. Final state
    await ctx.update_props("output", {"streaming": False})
    await ctx.update_text("status", "Complete")

async def stop_stream(ctx: Context):
    ctx.state.set("streaming_active", False)
```

### How `append_prop` Handles Different Types

```python
# String props — concatenated
await ctx.append_prop("my-md", "content", " World")
# before: "Hello" → after: "Hello World"

# List props — appended (single item) or extended (list)
await ctx.append_prop("my-chart", "data", {"x": 1, "y": 2})    # append one point
await ctx.append_prop("my-chart", "data", [{"x": 1}, {"x": 2}]) # extend

# Uninitialised props — inferred from value type
# String value → prop becomes string
# List value → prop becomes list
```

---

## 2. High-Frequency Streaming (30 fps Buffer)

When the source emits faster than once per 33ms, buffer chunks to avoid flooding the WebSocket:

```python
async def stream_fast(ctx: Context):
    import asyncio
    buf = ""
    t = asyncio.get_event_loop().time()
    
    async for chunk in fast_data_source():
        buf += chunk
        now = asyncio.get_event_loop().time()
        if now - t > 0.033:               # ~30 fps flush threshold
            await ctx.append_prop("output", "content", buf)
            buf = ""
            t = now
    
    # Flush remaining
    if buf:
        await ctx.append_prop("output", "content", buf)
```

---

## 3. Cancellable Streaming with Module-Level Flags

For per-session cancellation that doesn't require a `ctx.refresh()` call:

```python
_streaming_flags: dict[int, bool] = {}  # keyed by id(ctx)

async def start_stream(ctx: Context):
    _streaming_flags[id(ctx)] = True
    await ctx.update_props("output", {"content": "", "streaming": True})

    async for chunk in llm.stream(prompt):
        if not _streaming_flags.get(id(ctx), False):
            break
        await ctx.append_prop("output", "content", chunk)
    
    _streaming_flags.pop(id(ctx), None)
    await ctx.update_props("output", {"streaming": False})

async def stop_stream(ctx: Context):
    _streaming_flags[id(ctx)] = False
```

---

## 4. Streaming Chart Data

```python
MAX_POINTS = 20
chart_data: list[dict] = []

async def stream_chart(ctx: Context):
    global chart_data
    chart_data = []
    await ctx.update_props("live-chart", {"data": []})  # clear first

    for i in range(60):
        new_point = {
            "time": datetime.now().strftime("%H:%M:%S"),
            "value": round(50 + random.uniform(-20, 20), 1),
        }
        chart_data.append(new_point)

        if len(chart_data) > MAX_POINTS:
            chart_data = chart_data[-MAX_POINTS:]
            # Full replace when trimming to avoid stale points
            await ctx.update_props("live-chart", {"data": chart_data})
        else:
            # Cheap append when still filling up
            await ctx.append_prop("live-chart", "data", new_point)

        await asyncio.sleep(1)
```

---

## 5. Long-Running Tasks with Background Jobs

Use `asyncio.create_task()` for jobs that outlast the button click acknowledgement:

```python
@ui.page("/")
def page(ctx: Context):
    return rc.Column(children=[
        rc.Button("Start Job", id="start-btn", on_click=ctx.callback(start_job)),
        rc.Button("Stop", on_click=ctx.callback(stop_job)),
        rc.Progress(id="progress-bar", value=0, max=100, show_value=True),
        rc.Text(id="status", children="Idle"),
    ])

async def run_job(ctx: Context):
    """The actual background work."""
    try:
        ctx.state["stop_requested"] = False
        for i in range(10):
            if ctx.state.get("stop_requested"):
                await ctx.update_text("status", "Stopped.")
                await ctx.update_props("start-btn", {"loading": False})
                return
            
            await asyncio.sleep(1)
            pct = (i + 1) * 10
            await ctx.update_props("progress-bar", {"value": pct})
            await ctx.update_text("status", f"Processing step {i + 1}/10…")
        
        await ctx.update_text("status", "Complete!")
        await ctx.show_toast("Job finished!", variant="success")
    except Exception as e:
        # WebSocket may close before task finishes — always wrap in try/except
        print(f"Job error: {e}")
    finally:
        await ctx.update_props("start-btn", {"loading": False})

async def start_job(ctx: Context):
    await ctx.update_props("start-btn", {"loading": True})
    asyncio.create_task(run_job(ctx))  # returns immediately; button click acked

async def stop_job(ctx: Context):
    ctx.state["stop_requested"] = True
```

**Key rules for background tasks:**
1. `asyncio.create_task()` returns immediately → the triggering event is acknowledged right away.
2. All client communication must go through `ctx` methods.
3. **Always wrap the task body in `try/except`** — the WebSocket may close while the task is still running.
4. Use `ctx.state` as the stop-flag channel.

---

## 6. Realtime / Broadcast to All Clients

Push updates to every connected client using `ui.active_contexts`:

```python
# In a lifespan background task:
async def update_dashboard_task():
    while True:
        # Update global shared data
        global dashboard_data
        dashboard_data = fetch_live_data()

        # Push to ALL connected clients
        for ctx in ui.active_contexts:
            try:
                await ctx.replace("dashboard-root", render_dashboard(ctx))
            except Exception:
                pass  # client may have disconnected

        await asyncio.sleep(2)

@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(update_dashboard_task())
    yield
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass

app = FastAPI(lifespan=lifespan)
app.include_router(ui.router)
```

### Broadcast Toast or Simple Update

```python
async def notify_all(message: str):
    for ctx in ui.active_contexts:
        try:
            await ctx.show_toast(message, variant="info")
        except Exception:
            pass

async def broadcast_banner(ui: RefastApp, headline: str):
    for ctx in ui.active_contexts:
        try:
            await ctx.replace("news-banner", rc.Text(headline, class_name="font-bold"))
        except Exception:
            pass
```

### Per-Client State in Broadcast

Each `ctx` in `ui.active_contexts` still has independent `ctx.state`:

```python
for ctx in ui.active_contexts:
    try:
        # Per-client state is still accessible
        if not ctx.state.get("client_id"):
            ctx.state.set("client_id", f"#{random.randint(1000, 9999)}")
        
        await ctx.replace("root", render_for_client(ctx))
    except Exception:
        pass
```

---

## 7. Push Custom Events to the Frontend

```python
# In a callback — push a typed event to the browser's event system
async def data_ready(ctx: Context):
    result = await fetch_data()
    await ctx.push_event("data:ready", {"rows": result})
```

Custom JS on the frontend can listen for these events via Refast's event bus.

---

## 8. ScrollArea with `stick_to_bottom`

Pairs well with streaming output:

```python
rc.ScrollArea(
    id="chat-scroll",
    style={"height": "500px"},
    stick_to_bottom=ctx.state.get("sticky", True),  # default: scroll to bottom
    children=[
        rc.Column(id="messages", children=[...]),
    ],
)

# Toggle sticky from a switch
async def toggle_sticky(ctx: Context):
    checked = ctx.event_data  # True/False from Switch
    ctx.state.set("sticky", checked)
    await ctx.update_props("chat-scroll", {"stick_to_bottom": checked})
```

`stick_to_bottom` behaviour:
- While at the bottom: auto-scrolls on every new `append` / `append_prop`.
- If user scrolls up: stops auto-scrolling.
- If user scrolls back to bottom: resumes auto-scrolling.

---

## 9. Complete AI Chat Example Pattern

```python
import asyncio
from fastapi import FastAPI
from refast import RefastApp, Context
from refast import components as rc

ui = RefastApp(title="AI Chat", preloaded_features=["markdown"])

@ui.page("/")
def page(ctx: Context):
    messages = ctx.state.get("messages", [])
    is_streaming = ctx.state.get("streaming", False)
    return rc.Column(class_name="h-screen flex flex-col p-4 max-w-2xl mx-auto", children=[
        rc.Heading("AI Chat", level=1),
        rc.ScrollArea(
            id="chat-scroll",
            class_name="flex-1 border rounded",
            stick_to_bottom=True,
            children=[
                rc.Column(
                    id="messages",
                    class_name="p-4",
                    gap=3,
                    children=[
                        rc.Card(
                            class_name="ml-auto" if m["role"] == "user" else "",
                            children=[rc.Markdown(m["content"])],
                        )
                        for m in messages
                    ],
                ),
            ],
        ),
        rc.Row(gap=2, class_name="mt-2", children=[
            rc.Input(
                id="user-input",
                placeholder="Type a message...",
                on_change=ctx.save_prop("user_message"),
                disabled=is_streaming,
            ),
            rc.Button(
                "Send" if not is_streaming else "Stop",
                loading=is_streaming and False,
                on_click=ctx.callback(stop_stream if is_streaming else send_message,
                                      props=["user_message"]),
            ),
        ]),
    ])

_active_streams: dict[int, bool] = {}

async def send_message(ctx: Context, user_message: str = ""):
    if not user_message.strip():
        return
    
    # Add user message
    messages = ctx.state.get("messages", [])
    messages.append({"role": "user", "content": user_message})
    
    # Add empty assistant slot
    messages.append({"role": "assistant", "content": ""})
    ctx.state["messages"] = messages
    ctx.state["streaming"] = True
    await ctx.refresh()
    
    # Clear input
    await ctx.update_props("user-input", {"value": ""})
    
    # Stream response
    _active_streams[id(ctx)] = True
    asyncio.create_task(_stream_response(ctx))

async def _stream_response(ctx: Context):
    try:
        # Replace last assistant message with a streaming Markdown component
        msg_id = f"msg-{len(ctx.state.get('messages', []))}"
        await ctx.append("messages", rc.Card(
            children=[rc.Markdown(id=msg_id, content="", streaming=True)],
        ))
        
        async for chunk in my_llm.stream(ctx.state["messages"]):
            if not _active_streams.get(id(ctx), False):
                break
            await ctx.append_prop(msg_id, "content", chunk)
        
        await ctx.update_props(msg_id, {"streaming": False})
    except Exception as e:
        print(f"Stream error: {e}")
    finally:
        ctx.state["streaming"] = False
        _active_streams.pop(id(ctx), None)
        await ctx.refresh()

async def stop_stream(ctx: Context):
    _active_streams[id(ctx)] = False

app = FastAPI()
app.include_router(ui.router)
```
